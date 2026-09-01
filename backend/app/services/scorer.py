import re
from typing import Tuple, List, Optional
from app.models.profile import MatchReason
from app.models.search import SearchRequest
from app.config import settings

class ScoringEngine:
    """
    Transparent, multi-factor match scoring engine.
    Calculates 0-100 score and returns itemized match reasons.
    """
    
    @staticmethod
    def calculate_match_score(
        bio: str,
        display_name: str,
        tags: List[str],
        region: Optional[str],
        followers: Optional[int],
        request: SearchRequest
    ) -> Tuple[int, List[MatchReason], List[str]]:
        
        weights = settings.scoring_weights
        reasons: List[MatchReason] = []
        matched_keywords: List[str] = []
        
        full_text = f"{display_name or ''} {bio or ''} {' '.join(tags)}".lower()
        
        # 1. Niche Match (35% default weight)
        niche_score = 0.0
        niche_weight = weights.niche_weight * 100
        
        if not request.niche or not request.niche.strip():
            # If user didn't specify a niche, award baseline neutral points
            niche_score = niche_weight
            reasons.append(MatchReason(
                criterion="Niche",
                matched=True,
                description="No specific niche filter requested (full baseline)",
                score_contribution=niche_score
            ))
        else:
            niche_req = request.niche.strip().lower()
            if niche_req in [t.lower() for t in tags] or re.search(r'\b' + re.escape(niche_req) + r'\b', full_text):
                niche_score = niche_weight
                reasons.append(MatchReason(
                    criterion="Niche",
                    matched=True,
                    description=f"{request.niche.title()} niche detected in bio / tags",
                    score_contribution=niche_score
                ))
            elif any(t.lower() in full_text for t in tags if t.lower() != "open for collabs"):
                # Partial adjacent niche overlap
                niche_score = niche_weight * 0.5
                reasons.append(MatchReason(
                    criterion="Niche",
                    matched=False,
                    description=f"Adjacent creative content detected (target: {request.niche.title()})",
                    score_contribution=niche_score
                ))
            else:
                reasons.append(MatchReason(
                    criterion="Niche",
                    matched=False,
                    description=f"No explicit {request.niche.title()} keywords detected",
                    score_contribution=0.0
                ))
                
        # 2. Region Match (25% default weight)
        region_score = 0.0
        region_weight = weights.region_weight * 100
        
        if not request.region or not request.region.strip():
            region_score = region_weight
            reasons.append(MatchReason(
                criterion="Region",
                matched=True,
                description="No specific region filter requested (open discovery)",
                score_contribution=region_score
            ))
        else:
            region_req = request.region.strip().lower()
            if (region and region.lower() == region_req) or re.search(r'\b' + re.escape(region_req) + r'\b', full_text):
                region_score = region_weight
                reasons.append(MatchReason(
                    criterion="Region",
                    matched=True,
                    description=f"{request.region.title()} regional signal detected",
                    score_contribution=region_score
                ))
            else:
                reasons.append(MatchReason(
                    criterion="Region",
                    matched=False,
                    description=f"No explicit {request.region.title()} region signal found in public snippet",
                    score_contribution=0.0
                ))

        # 3. Follower Range Match (20% default weight)
        follower_score = 0.0
        follower_weight = weights.follower_weight * 100
        has_min = request.followers_min is not None and request.followers_min > 0
        has_max = request.followers_max is not None and request.followers_max > 0
        
        if not has_min and not has_max:
            follower_score = follower_weight
            reasons.append(MatchReason(
                criterion="Followers",
                matched=True,
                description="Any audience size permitted",
                score_contribution=follower_score
            ))
        elif followers is None:
            # Unindexed follower count in public search snippet - give partial neutral baseline
            follower_score = follower_weight * 0.4
            reasons.append(MatchReason(
                criterion="Followers",
                matched=False,
                description="Follower count not publicly indexed in search snippet (partial neutral score)",
                score_contribution=follower_score
            ))
        else:
            min_val = request.followers_min or 0
            max_val = request.followers_max or float('inf')
            max_val_str = f"{int(max_val):,}" if max_val != float('inf') else "500k+"
            range_str = f"{min_val:,} - {max_val_str}"
            
            if min_val <= followers <= max_val:
                follower_score = follower_weight
                reasons.append(MatchReason(
                    criterion="Followers",
                    matched=True,
                    description=f"Audience ({followers:,}) within target range ({range_str})",
                    score_contribution=follower_score
                ))
            else:
                # Check if it is close (within 20% margin)
                if (followers < min_val and followers >= min_val * 0.8) or (followers > max_val and followers <= max_val * 1.2):
                    follower_score = follower_weight * 0.5
                    reasons.append(MatchReason(
                        criterion="Followers",
                        matched=False,
                        description=f"Audience ({followers:,}) slightly outside target bracket",
                        score_contribution=follower_score
                    ))
                else:
                    reasons.append(MatchReason(
                        criterion="Followers",
                        matched=False,
                        description=f"Audience ({followers:,}) outside target bracket ({range_str})",
                        score_contribution=0.0
                    ))

        # 4. Keyword Match (20% default weight)
        keyword_score = 0.0
        keyword_weight = weights.keyword_weight * 100
        
        if not request.keywords or len(request.keywords) == 0:
            keyword_score = keyword_weight
            reasons.append(MatchReason(
                criterion="Keywords",
                matched=True,
                description="No specific custom keywords requested",
                score_contribution=keyword_score
            ))
        else:
            matched_count = 0
            for kw in request.keywords:
                clean_kw = kw.strip().lower()
                if clean_kw and re.search(r'\b' + re.escape(clean_kw) + r'\b', full_text):
                    matched_count += 1
                    matched_keywords.append(kw.strip())
                    
            if matched_count > 0:
                fraction = matched_count / len(request.keywords)
                keyword_score = keyword_weight * fraction
                reasons.append(MatchReason(
                    criterion="Keywords",
                    matched=True,
                    description=f"Matched {matched_count}/{len(request.keywords)} keywords: {', '.join(matched_keywords)}",
                    score_contribution=keyword_score
                ))
            else:
                reasons.append(MatchReason(
                    criterion="Keywords",
                    matched=False,
                    description=f"No matches for requested keywords ({', '.join(request.keywords)})",
                    score_contribution=0.0
                ))

        raw_total = niche_score + region_score + follower_score + keyword_score
        final_score = max(0, min(100, int(round(raw_total))))
        
        return final_score, reasons, matched_keywords
