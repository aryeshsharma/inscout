import logging
from typing import Tuple, List, Optional
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
    and optional Meta API enrichment.
    """
    
    def __init__(self):
        self.search_provider = SearchDiscoveryProvider()
        self.meta_provider = MetaInstagramProvider()
        
    def get_provider(self, name: str = "search") -> BaseDiscoveryProvider:
        return self.search_provider

    async def execute_discovery(
        self, request: SearchRequest
    ) -> Tuple[List[DiscoveredProfile], str, bool, Optional[str], int, int, int]:
        
        warning: Optional[str] = None
        
        try:
            profiles, candidates_count, verified_count, matched_count = (
                await self.search_provider.discover_profiles_with_metrics(request)
            )
            
            if not profiles or len(profiles) == 0:
                logger.info("Public web discovery returned 0 matching candidates.")
                return [], "search", False, None, candidates_count, verified_count, matched_count
                
            return profiles, "search", False, None, candidates_count, verified_count, matched_count
            
        except Exception as e:
            logger.error(f"Live search discovery error: {e}")
            warning = "Live public discovery is currently unavailable."
            return [], "search", False, warning, 0, 0, 0
