import asyncio
import logging
import urllib.parse
import re
from typing import List, Set, Dict, Any
import httpx
from bs4 import BeautifulSoup

from app.discovery.base import BaseDiscoveryProvider
from app.models.profile import DiscoveredProfile
from app.models.search import SearchRequest
from app.services.query_generator import QueryGenerator
from app.services.normalizer import ProfileNormalizer, RESERVED_USERNAMES
from app.services.tagger import TaggingEngine
from app.services.scorer import ScoringEngine

logger = logging.getLogger("inscout.search_provider")

RESERVED_USERNAMES.update({
    "popular", "topics", "channel", "guides", "directory", "about", "blog",
    "tags", "explore", "reels", "p", "stories", "locations", "accounts",
    "legal", "privacy", "terms", "help", "instagram"
})

class SearchDiscoveryProvider(BaseDiscoveryProvider):
    """
    Public web search engine discovery provider.
    Discovers candidate real Instagram profiles via free public web search indexes.
    """
    
    @property
    def provider_name(self) -> str:
        return "search"
        
    @property
    def is_demo(self) -> bool:
        return False

    async def discover_profiles(self, request: SearchRequest) -> List[DiscoveredProfile]:
        layered_queries = QueryGenerator.generate_layered_queries(request)
        logger.info(f"Executing public web discovery with queries: {layered_queries}")
        
        raw_items: List[Dict[str, Any]] = []
        seen_urls: Set[str] = set()

        for q in layered_queries:
            if len(raw_items) >= request.max_results:
                break
                
            # Query public search sources
            results = await self._search_multi_source(q)
            for r in results:
                url = r.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    raw_items.append(r)
                    
            await asyncio.sleep(0.4)

        seen_usernames: Set[str] = set()
        discovered_profiles: List[DiscoveredProfile] = []

        for item in raw_items:
            url = item.get("url", "")
            username = ProfileNormalizer.extract_username_from_url(url)
            
            if not username or username in seen_usernames or username in RESERVED_USERNAMES:
                continue
                
            seen_usernames.add(username)
            
            title = item.get("title", "")
            raw_body = item.get("snippet", "") or item.get("body", "")
            
            display_name = ProfileNormalizer.extract_display_name(title, username)
            followers = ProfileNormalizer.parse_follower_count(f"{title} {raw_body}")
            clean_bio = ProfileNormalizer.clean_bio_snippet(raw_body)
            
            # Detect region from snippet text, or check if user query region matches
            detected_region = TaggingEngine.detect_region(f"{title} {clean_bio}")
            if not detected_region and request.region and "any region" not in request.region.lower():
                clean_req_reg = request.region.strip().lower()
                if clean_req_reg in f"{title} {clean_bio}".lower():
                    detected_region = request.region.title()
                
            # Extract tags using deterministic taxonomy
            tags = TaggingEngine.extract_tags(
                text=f"{title} {clean_bio}",
                user_query_niche=request.niche or "",
                user_keywords=request.keywords
            )
            
            # Calculate match score & reasons
            score, reasons, matched_kws = ScoringEngine.calculate_match_score(
                bio=clean_bio,
                display_name=display_name or username,
                tags=tags,
                region=detected_region,
                followers=followers,
                request=request
            )
            
            # Evaluate data confidence
            conf_level, conf_details = ProfileNormalizer.evaluate_confidence(
                has_bio=bool(clean_bio),
                has_followers=followers is not None,
                has_region_signal=bool(detected_region),
                is_direct_profile=True
            )
            
            profile = DiscoveredProfile(
                username=username,
                profile_url=f"https://www.instagram.com/{username}/",
                display_name=display_name,
                bio=clean_bio if clean_bio else None,
                followers=followers,
                followers_formatted=ProfileNormalizer.format_followers(followers),
                region=detected_region if detected_region else None,
                tags=tags,
                matched_keywords=matched_kws,
                match_score=score,
                match_reasons=reasons,
                data_confidence=conf_level,
                confidence_details=conf_details,
                is_demo=False,
                profile_image=None # Real data only; not fabricated
            )
            
            discovered_profiles.append(profile)

        # Sort candidate results by Match Score
        discovered_profiles.sort(key=lambda p: p.match_score, reverse=True)
        return discovered_profiles[:request.max_results]

    async def _search_multi_source(self, query: str) -> List[Dict[str, Any]]:
        """
        Queries resilient free public web search endpoints asynchronously.
        """
        def _sync_fetch() -> List[Dict[str, Any]]:
            items: List[Dict[str, Any]] = []
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            # Source 1: Brave public web HTML search
            try:
                brave_url = f"https://search.brave.com/search?q={urllib.parse.quote(query)}"
                with httpx.Client(headers=headers, timeout=6.0, follow_redirects=True) as client:
                    resp = client.get(brave_url)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, "html.parser")
                        for snippet_div in soup.select("div.snippet"):
                            a_tag = snippet_div.select_one("a")
                            title_div = snippet_div.select_one(".title, h2, h3")
                            desc_div = snippet_div.select_one(".snippet-description, .content")
                            if a_tag:
                                href = a_tag.get("href", "")
                                if "instagram.com" in href:
                                    u = ProfileNormalizer.extract_username_from_url(href)
                                    if u and u not in RESERVED_USERNAMES:
                                        items.append({
                                            "url": f"https://www.instagram.com/{u}/",
                                            "title": title_div.get_text(strip=True) if title_div else a_tag.get_text(strip=True),
                                            "snippet": desc_div.get_text(strip=True) if desc_div else ""
                                        })
            except Exception as e:
                logger.debug(f"Brave error: {e}")

            # Source 2: Mojeek public HTML search
            if len(items) < 3:
                try:
                    mojeek_url = f"https://www.mojeek.com/search?q={urllib.parse.quote(query)}"
                    with httpx.Client(headers=headers, timeout=6.0, follow_redirects=True) as client:
                        resp = client.get(mojeek_url)
                        if resp.status_code == 200:
                            soup = BeautifulSoup(resp.text, "html.parser")
                            for a_tag in soup.select("a.ob"):
                                href = a_tag.get("href", "")
                                if "instagram.com" in href:
                                    u = ProfileNormalizer.extract_username_from_url(href)
                                    if u and u not in RESERVED_USERNAMES:
                                        p_desc = a_tag.find_next_sibling("p", class_="s")
                                        items.append({
                                            "url": f"https://www.instagram.com/{u}/",
                                            "title": a_tag.get_text(strip=True),
                                            "snippet": p_desc.get_text(strip=True) if p_desc else ""
                                        })
                except Exception as e:
                    logger.debug(f"Mojeek error: {e}")

            # Source 3: DuckDuckGo text search
            if len(items) < 3:
                try:
                    from duckduckgo_search import DDGS
                    with DDGS() as ddgs:
                        for r in ddgs.text(query, max_results=15):
                            href = r.get("href", "")
                            if "instagram.com" in href:
                                u = ProfileNormalizer.extract_username_from_url(href)
                                if u and u not in RESERVED_USERNAMES:
                                    items.append({
                                        "url": f"https://www.instagram.com/{u}/",
                                        "title": r.get("title", ""),
                                        "snippet": r.get("body", "")
                                    })
                except Exception as e:
                    logger.debug(f"DDGS error: {e}")

            return items

        return await asyncio.to_thread(_sync_fetch)
