import logging
from typing import Tuple, List, Optional, Dict, Any
from app.discovery.base import BaseDiscoveryProvider
from app.discovery.search_provider import SearchDiscoveryProvider
from app.discovery.meta_provider import MetaInstagramProvider
from app.models.profile import DiscoveredProfile
from app.models.search import SearchRequest

logger = logging.getLogger("inscout.discovery_engine")

class DiscoveryEngine:
    """
    Discovery Engine V2 Coordinator.
    Orchestrates high-volume candidate discovery, deduplication, verification,
    hard filtering, scoring, and optional Meta API enrichment.
    """
    
    def __init__(self):
        self.search_provider = SearchDiscoveryProvider()
        self.meta_provider = MetaInstagramProvider()
        
    def get_provider(self, name: str = "search") -> BaseDiscoveryProvider:
        return self.search_provider

    async def execute_discovery(
        self, request: SearchRequest
    ) -> Dict[str, Any]:
        
        warning: Optional[str] = None
        
        try:
            (
                profiles,
                c_disc,
                u_cand,
                p_ver,
                f_pass,
                rn_pass,
                q_gen,
                q_exec,
                pag_used
            ) = await self.search_provider.discover_profiles_with_metrics(request)
            
            p_rejected = max(0, p_ver - rn_pass)
            p_matched = rn_pass
            p_returned = len(profiles)

            return {
                "profiles": profiles,
                "provider_used": "search",
                "is_demo": False,
                "warning": warning,
                "candidates_discovered": c_disc,
                "unique_candidates": u_cand,
                "profiles_verified": p_ver,
                "profiles_rejected": p_rejected,
                "follower_filter_passed": f_pass,
                "region_niche_passed": rn_pass,
                "profiles_matched": p_matched,
                "profiles_returned": p_returned,
                "queries_generated": q_gen,
                "queries_executed": q_exec,
                "pagination_used": pag_used,
                "discovery_sources": ["public_web_search", "creator_index"]
            }
            
        except Exception as e:
            logger.error(f"Live search discovery error: {e}")
            warning = "Live public discovery encountered a temporary issue."
            return {
                "profiles": [],
                "provider_used": "search",
                "is_demo": False,
                "warning": warning,
                "candidates_discovered": 0,
                "unique_candidates": 0,
                "profiles_verified": 0,
                "profiles_rejected": 0,
                "follower_filter_passed": 0,
                "region_niche_passed": 0,
                "profiles_matched": 0,
                "profiles_returned": 0,
                "queries_generated": 0,
                "queries_executed": 0,
                "pagination_used": False,
                "discovery_sources": ["public_web_search"]
            }
