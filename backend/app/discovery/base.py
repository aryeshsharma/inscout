from abc import ABC, abstractmethod
from typing import List
from app.models.profile import DiscoveredProfile
from app.models.search import SearchRequest

class BaseDiscoveryProvider(ABC):
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the discovery provider."""
        pass
        
    @property
    @abstractmethod
    def is_demo(self) -> bool:
        """Whether this provider yields simulated/demo data."""
        pass

    @abstractmethod
    async def discover_profiles(self, request: SearchRequest) -> List[DiscoveredProfile]:
        """
        Executes discovery against the underlying public or simulated data source.
        Returns a list of normalized DiscoveredProfile candidates.
        """
        pass
