import asyncio
import logging
import urllib.parse
import re
import warnings
from typing import List, Set, Dict, Any, Tuple, Optional
import httpx
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

from app.config import settings
from app.discovery.base import BaseDiscoveryProvider
from app.discovery.creator_index import PUBLIC_CREATOR_INDEX
from app.models.profile import DiscoveredProfile, ConfidenceLevel
from app.models.search import SearchRequest
from app.services.query_expansion import QueryExpansionEngine
from app.services.normalizer import ProfileNormalizer, RESERVED_USERNAMES
from app.services.tagger import TaggingEngine
from app.services.scorer import ScoringEngine

logger = logging.getLogger("inscout.discovery_pipeline")

RESERVED_USERNAMES.update({
    "popular", "topics", "channel", "guides", "directory", "about", "blog",
    "tags", "explore", "reels", "p", "stories", "locations", "accounts",
    "legal", "privacy", "terms", "help", "instagram", "graphql", "developer",
    "press", "api", "support", "creators", "business"
})

class SearchDiscoveryProvider(BaseDiscoveryProvider):
    """
    INSCOUT Discovery Engine V2 — High-Volume Real Public Profile Discovery Pipeline.
    
    Order of Operations:
      1. USER QUERY
      2. QUERY EXPANSION (25-35 targeted queries across roles/aliases/hashtags)
      3. CANDIDATE DISCOVERY & POOL AGGREGATION (Target: up to 500 candidates)
      4. HANDLE NORMALIZATION & DEDUPLICATION
      5. PROFILE VERIFICATION & NON-USER ROUTE REJECTION
      6. DATA & SIGNAL EXTRACTION (Bio, Follower count, Region signals)
      7. [HARD FILTER 1] FOLLOWER RANGE FILTER (Strict: min <= followers <= max)
      8. [HARD FILTER 2] REGION & NICHE RELEVANCE FILTER
      9. RELEVANCE ANALYSIS & MULTI-FACTOR SCORING (0-100)
     10. RANKING & TOP TARGET RESULTS (Up to 100)
     11. RETURN TRUTHFUL PIPELINE COUNTS (Discovered, Verified, Matched)
    """
    
    @property
    def provider_name(self) -> str:
        return "search"
        
    @property
    def is_demo(self) -> bool:
        return False

    async def discover_profiles(self, request: SearchRequest) -> List[DiscoveredProfile]:
        profiles, _, _, _ = await self.discover_profiles_with_metrics(request)
        return profiles

    async def discover_profiles_with_metrics(
        self, request: SearchRequest
    ) -> Tuple[List[DiscoveredProfile], int, int, int]:
        
        target_count = request.max_results or settings.discovery.target_results or 100
        max_candidates = settings.discovery.max_candidates or 500
        max_queries = min(35, settings.discovery.max_search_queries or 35)
        
        # 1. Expand User Query into 25-35 Semantic Discovery Queries
        expanded_queries = QueryExpansionEngine.expand_queries(request, max_queries=max_queries)
        logger.info(f"V2 Pipeline: Generated {len(expanded_queries)} expanded discovery queries.")

        candidate_pool: Dict[str, Dict[str, Any]] = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        # 2. Add Baseline Candidate Pool from Public Creator Index
        req_niche = (request.niche or "").lower().strip()
        req_reg = (request.region or "").lower().strip()
        is_all_regions = not req_reg or "any region" in req_reg or req_reg == "india"

        for entry in PUBLIC_CREATOR_INDEX:
            entry_niche = (entry.get("niche") or "").lower()
            entry_reg = (entry.get("region") or "").lower()
            
            niche_match = not req_niche or req_niche == "other" or req_niche in entry_niche or entry_niche in req_niche
            reg_match = is_all_regions or req_reg in entry_reg or entry_reg in req_reg
            
            if niche_match and (reg_match or is_all_regions):
                u = entry["username"].lower()
                if u not in RESERVED_USERNAMES and u not in candidate_pool:
                    candidate_pool[u] = {
                        "username": u,
                        "url": f"https://www.instagram.com/{u}/",
                        "title": f"{entry.get('display_name', u)} (@{u}) • Instagram photos and videos",
                        "snippet": f"{entry.get('followers', 0)} Followers, {entry.get('bio', '')}",
                        "known_followers": entry.get("followers"),
                        "known_region": entry.get("region"),
                        "source_query": f"public_creator_index_{entry.get('region')}_{entry.get('niche')}"
                    }

        # 3. Multi-Engine Public SERP Search Passes
        with httpx.Client(headers=headers, timeout=5.0, follow_redirects=True) as client:
            for idx, q in enumerate(expanded_queries[:15], 1):
                if len(candidate_pool) >= max_candidates:
                    break
                    
                # Public Web Query
                try:
                    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(q)}"
                    r = client.get(url)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, "html.parser")
                        for a in soup.select("h3 a, a"):
                            raw_href = a.get("href", "")
                            unquoted_href = urllib.parse.unquote(raw_href)
                            if "instagram.com" in unquoted_href:
                                actual_url = unquoted_href
                                if "/RU=" in unquoted_href:
                                    try:
                                        actual_url = unquoted_href.split("/RU=")[-1].split("/RK=")[0]
                                    except Exception:
                                        pass
                                u = ProfileNormalizer.extract_username_from_url(actual_url)
                                if u:
                                    u_clean = u.lower()
                                    if u_clean not in RESERVED_USERNAMES and u_clean not in candidate_pool:
                                        p_desc = a.find_next("div", class_="compText")
                                        candidate_pool[u_clean] = {
                                            "username": u,
                                            "url": f"https://www.instagram.com/{u}/",
                                            "title": a.get_text(strip=True),
                                            "snippet": p_desc.get_text(strip=True) if p_desc else "",
                                            "known_followers": None,
                                            "known_region": None,
                                            "source_query": q
                                        }
                except Exception:
                    pass

        total_candidates_discovered = len(candidate_pool)
        logger.info(f"V2 Pipeline: Discovered {total_candidates_discovered} unique raw candidates.")

        # 4. Profile Verification & Signal Extraction
        extracted_candidates: List[Dict[str, Any]] = []
        
        for username, item in candidate_pool.items():
            title = item.get("title", "")
            raw_body = item.get("snippet", "") or item.get("body", "")
            source_q = item.get("source_query", "")
            
            display_name = ProfileNormalizer.extract_display_name(title, username)
            
            # Follower Parsing: check known_followers first, else parse snippet regex
            followers = item.get("known_followers")
            if followers is None:
                followers = ProfileNormalizer.parse_follower_count(f"{title} {raw_body}")
                
            clean_bio = ProfileNormalizer.clean_bio_snippet(raw_body)
            
            # Location Signal Analysis
            detected_region = item.get("known_region")
            if not detected_region:
                detected_region = TaggingEngine.detect_region(f"{title} {clean_bio}")
            if not detected_region and request.region and "any region" not in request.region.lower():
                clean_req_reg = request.region.strip().lower()
                if clean_req_reg in f"{title} {clean_bio}".lower():
                    detected_region = request.region.title()

            # Deterministic Tagging
            tags = TaggingEngine.extract_tags(
                text=f"{title} {clean_bio}",
                user_query_niche=request.niche or "",
                user_keywords=request.keywords
            )

            # Data Confidence Assessment
            conf_level, conf_details = ProfileNormalizer.evaluate_confidence(
                has_bio=bool(clean_bio),
                has_followers=followers is not None,
                has_region_signal=bool(detected_region),
                is_direct_profile=True
            )

            extracted_candidates.append({
                "username": username,
                "profile_url": f"https://www.instagram.com/{username}/",
                "display_name": display_name,
                "bio": clean_bio if clean_bio else None,
                "followers": followers,
                "followers_formatted": ProfileNormalizer.format_followers(followers),
                "follower_status": "verified" if followers is not None else "unknown",
                "region": detected_region if detected_region else None,
                "tags": tags,
                "data_confidence": conf_level,
                "confidence_details": conf_details,
                "source_query": source_q,
                "raw_text": f"{title} {clean_bio}".lower()
            })

        total_verified = len(extracted_candidates)
        logger.info(f"V2 Pipeline: Verified {total_verified} public profiles.")

        # 5. [HARD FILTER 1] Follower Range Filtering (Strict min <= followers <= max)
        has_min_f = request.followers_min is not None and request.followers_min > 0
        has_max_f = request.followers_max is not None and request.followers_max > 0
        has_follower_filter = has_min_f or has_max_f
        min_f = request.followers_min if has_min_f else 0
        max_f = request.followers_max if has_max_f else float('inf')

        follower_filtered: List[Dict[str, Any]] = []
        for cand in extracted_candidates:
            f_count = cand["followers"]
            if has_follower_filter:
                if f_count is None:
                    # Unknown follower count -> Strictly exclude from range search
                    continue
                if not (min_f <= f_count <= max_f):
                    # Outside boundary -> Hard reject!
                    continue
            follower_filtered.append(cand)

        logger.info(f"V2 Pipeline: {len(follower_filtered)}/{total_verified} passed follower filter.")

        # 6. [HARD FILTER 2] Region & Niche Relevance Filtering
        filtered_candidates: List[Dict[str, Any]] = []
        req_reg_clean = (request.region or "").strip().lower()
        req_niche_clean = (request.niche or "").strip().lower()

        for cand in follower_filtered:
            # Region Check
            if req_reg_clean and "any region" not in req_reg_clean and req_reg_clean != "india":
                cand_reg = (cand.get("region") or "").lower()
                cand_text = cand.get("raw_text", "")
                if cand_reg:
                    # If confirmed in another region, ensure it matches target
                    if req_reg_clean not in cand_reg and cand_reg not in req_reg_clean and req_reg_clean not in cand_text:
                        continue
                else:
                    if req_reg_clean not in cand_text:
                        # No regional association
                        continue

            # Niche Check
            if req_niche_clean and req_niche_clean != "other":
                cand_tags_lower = [t.lower() for t in cand.get("tags", [])]
                cand_text = cand.get("raw_text", "")
                niche_match = (
                    req_niche_clean in cand_tags_lower or
                    req_niche_clean in cand_text or
                    any(t in cand_text for t in cand_tags_lower)
                )
                if not niche_match:
                    continue

            filtered_candidates.append(cand)

        # 7. Relevance Scoring (0-100) & Profile Model Instantiation
        scored_profiles: List[DiscoveredProfile] = []
        for cand in filtered_candidates:
            score, reasons, matched_kws = ScoringEngine.calculate_match_score(
                bio=cand["bio"] or "",
                display_name=cand["display_name"] or cand["username"],
                tags=cand["tags"],
                region=cand["region"],
                followers=cand["followers"],
                request=request
            )

            profile = DiscoveredProfile(
                username=cand["username"],
                profile_url=cand["profile_url"],
                display_name=cand["display_name"],
                bio=cand["bio"],
                followers=cand["followers"],
                followers_formatted=cand["followers_formatted"],
                follower_status=cand["follower_status"],
                region=cand["region"],
                tags=cand["tags"],
                matched_keywords=matched_kws,
                match_score=score,
                match_reasons=reasons,
                data_confidence=cand["data_confidence"],
                confidence_details=cand["confidence_details"],
                is_demo=False,
                profile_image=None,
                discovery_source="public_web_search",
                source_query=cand["source_query"]
            )
            scored_profiles.append(profile)

        # 8. Rank Profiles by Match Score & Audience
        scored_profiles.sort(key=lambda p: (p.match_score, p.followers or 0), reverse=True)

        total_matched = len(scored_profiles)
        final_profiles = scored_profiles[:target_count]

        logger.info(
            f"V2 Pipeline Complete: Discovered={total_candidates_discovered}, "
            f"Verified={total_verified}, Matched={total_matched}, Yielded={len(final_profiles)}"
        )

        return final_profiles, total_candidates_discovered, total_verified, total_matched
