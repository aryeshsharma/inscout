import logging
from typing import Dict, Any, Optional
from app.discovery.base import BaseDiscoveryProvider
from app.discovery.search_provider import SearchDiscoveryProvider
from app.discovery.meta_provider import MetaInstagramProvider
from app.models.search import SearchRequest

logger = logging.getLogger("inscout.discovery_engine")

class DiscoveryEngine:
    """
    Discovery Engine Coordinator (V3 Pure Live Architecture).
    Orchestrates pure live public candidate discovery, deduplication, verification,
    strict hard filtering, scoring, and optional Meta API enrichment.
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
            discovery_data = await self.search_provider.discover_profiles_with_metrics(request)
            discovery_data["provider_used"] = "search"
            discovery_data["is_demo"] = False
            discovery_data["warning"] = None
            return discovery_data
            
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
                "rejection_breakdown": {},
                "follower_filter_passed": 0,
                "region_niche_passed": 0,
                "profiles_matched": 0,
                "profiles_returned": 0,
                "queries_generated": 0,
                "queries_executed": 0,
                "pagination_used": False,
                "region_username_bias_pct": 0.0,
                "bio_location_evidence_pct": 100.0,
                "discovery_sources": ["public_web_search"]
            }
