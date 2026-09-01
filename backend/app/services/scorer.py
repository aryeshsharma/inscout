import re
from typing import Tuple, List, Optional
from app.models.profile import MatchReason, ConfidenceLevel
from app.models.search import SearchRequest

class ScoringEngine:
    """
    INSCOUT Transparent Multi-Factor Match Scoring Engine (Post-Hard-Filter).
    
    Weights:
      1. Niche Relevance: 35%
      2. Geographic Relevance (Bio-verified only): 30%
      3. Bio Keyword Relevance: 20%
      4. Data Confidence: 15%
      
    Follower count is a HARD FILTER (0% score contribution).
    Username/handle contributes ZERO to geographic relevance.
    """
    
    @staticmethod
    def calculate_match_score(
        bio: Optional[str],
        display_name: Optional[str],
        tags: List[str],
        region: Optional[str],
        region_confidence: str,
        data_confidence: ConfidenceLevel,
        request: SearchRequest
    ) -> Tuple[int, List[MatchReason], List[str]]:
        
        reasons: List[MatchReason] = []
        matched_keywords: List[str] = []
        
        bio_clean = (bio or "").lower()
        tags_clean = [t.lower() for t in tags]
        
        # 1. Niche Relevance (35% weight)
        niche_score = 0.0
        niche_weight = 35.0
        
        if not request.niche or not request.niche.strip():
            niche_score = niche_weight
            reasons.append(MatchReason(
                criterion="Niche",
                matched=True,
                description="No specific niche filter requested (full baseline)",
                score_contribution=niche_score
            ))
        else:
            niche_req = request.niche.strip().lower()
            if niche_req in tags_clean or re.search(r'\b' + re.escape(niche_req) + r'\b', bio_clean):
                niche_score = niche_weight
                reasons.append(MatchReason(
                    criterion="Niche",
                    matched=True,
                    description=f"{request.niche.title()} niche verified in bio / content tags",
                    score_contribution=niche_score
                ))
            elif any(t in bio_clean for t in tags_clean if t != "open for collabs"):
                niche_score = niche_weight * 0.6
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
                    description=f"No explicit {request.niche.title()} keywords detected in bio",
                    score_contribution=0.0
                ))
                
        # 2. Geographic Relevance (30% weight) — STRICTLY BIO-VERIFIED
        region_score = 0.0
        region_weight = 30.0
        
        if not request.region or not request.region.strip() or "any region" in request.region.lower() or request.region.lower() == "india":
            region_score = region_weight
            reasons.append(MatchReason(
                criterion="Region",
                matched=True,
                description="Open nationwide discovery (full baseline)",
                score_contribution=region_score
            ))
        else:
            req_reg = request.region.strip().lower()
            cand_reg = (region or "").lower()
            
            # Geographic points are awarded ONLY if confirmed by bio/snippet signals with HIGH/MEDIUM confidence
            if cand_reg == req_reg and region_confidence == "HIGH":
                region_score = region_weight
                reasons.append(MatchReason(
                    criterion="Region",
                    matched=True,
                    description=f"High-confidence location verified in bio ({request.region.title()})",
                    score_contribution=region_score
                ))
            elif cand_reg == req_reg and region_confidence == "MEDIUM":
                region_score = region_weight * 0.8
                reasons.append(MatchReason(
                    criterion="Region",
                    matched=True,
                    description=f"Regional NCR / cluster signal detected in bio ({request.region.title()})",
                    score_contribution=region_score
                ))
            else:
                reasons.append(MatchReason(
                    criterion="Region",
                    matched=False,
                    description=f"No verified {request.region.title()} location signal in bio text",
                    score_contribution=0.0
                ))

        # 3. Bio Keyword Relevance (20% weight) — SEMANTIC CONCEPT MATCHING
        keyword_score = 0.0
        keyword_weight = 20.0
        
        if not request.keywords or len(request.keywords) == 0:
            keyword_score = keyword_weight
            reasons.append(MatchReason(
                criterion="Keywords",
                matched=True,
                description="No specific custom bio keywords requested",
                score_contribution=keyword_score
            ))
        else:
            matched_count = 0
            for kw in request.keywords:
                clean_kw = kw.strip().lower()
                if clean_kw and (re.search(r'\b' + re.escape(clean_kw) + r'\b', bio_clean) or clean_kw in tags_clean):
                    matched_count += 1
                    matched_keywords.append(kw.strip())
                    
            if matched_count > 0:
                fraction = matched_count / len(request.keywords)
                keyword_score = keyword_weight * fraction
                reasons.append(MatchReason(
                    criterion="Keywords",
                    matched=True,
                    description=f"Matched {matched_count}/{len(request.keywords)} bio concepts: {', '.join(matched_keywords)}",
                    score_contribution=keyword_score
                ))
            else:
                reasons.append(MatchReason(
                    criterion="Keywords",
                    matched=False,
                    description=f"No matches for requested keywords ({', '.join(request.keywords)}) in bio",
                    score_contribution=0.0
                ))

        # 4. Data Confidence (15% weight)
        confidence_score = 0.0
        confidence_weight = 15.0
        
        if data_confidence == ConfidenceLevel.HIGH:
            confidence_score = confidence_weight
            reasons.append(MatchReason(
                criterion="Data Confidence",
                matched=True,
                description="High data confidence (verified bio, audience, and public signals)",
                score_contribution=confidence_score
            ))
        elif data_confidence == ConfidenceLevel.MEDIUM:
            confidence_score = confidence_weight * 0.7
            reasons.append(MatchReason(
                criterion="Data Confidence",
                matched=True,
                description="Medium data confidence (standard public index signals)",
                score_contribution=confidence_score
            ))
        else:
            confidence_score = confidence_weight * 0.3
            reasons.append(MatchReason(
                criterion="Data Confidence",
                matched=False,
                description="Low data confidence (minimal public snippet)",
                score_contribution=confidence_score
            ))

        raw_total = niche_score + region_score + keyword_score + confidence_score
        final_score = max(0, min(100, int(round(raw_total))))
        
        return final_score, reasons, matched_keywords
