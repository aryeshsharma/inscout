import logging
from typing import Tuple, List, Optional
from app.discovery.base import BaseDiscoveryProvider
from app.discovery.search_provider import SearchDiscoveryProvider
from app.models.profile import DiscoveredProfile
from app.models.search import SearchRequest

logger = logging.getLogger("inscout.discovery_engine")

class DiscoveryEngine:
    """
    Coordinates real public web discovery for Instagram profiles.
    Strictly adheres to data transparency: never fabricates results or silently falls back to demo data.
    """
    
    def __init__(self):
        self.search_provider = SearchDiscoveryProvider()
        
    def get_provider(self, name: str = "search") -> BaseDiscoveryProvider:
        return self.search_provider

    async def execute_discovery(
        self, request: SearchRequest
    ) -> Tuple[List[DiscoveredProfile], str, bool, Optional[str]]:
        
        warning: Optional[str] = None
        
        try:
            profiles = await self.search_provider.discover_profiles(request)
            if not profiles or len(profiles) == 0:
                logger.info("Public web discovery returned 0 matching candidates.")
                return [], "search", False, None
                
            return profiles, "search", False, None
            
        except Exception as e:
            logger.error(f"Live search discovery error: {e}")
            warning = "Live public discovery is currently unavailable."
            return [], "search", False, warning
