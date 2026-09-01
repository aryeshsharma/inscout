from typing import Dict, Optional
from app.models.response import SearchResponse
from app.models.profile import DiscoveredProfile

class SessionStore:
    """
    In-memory session storage for search results.
    Enables rapid filtering, sorting, profile lookup, and CSV export.
    """
    def __init__(self):
        self._searches: Dict[str, SearchResponse] = {}
        self._profiles_cache: Dict[str, DiscoveredProfile] = {}

    def save_search(self, search_id: str, response: SearchResponse):
        self._searches[search_id] = response
        for p in response.profiles:
            self._profiles_cache[p.username.lower()] = p

    def get_search(self, search_id: str) -> Optional[SearchResponse]:
        return self._searches.get(search_id)

    def get_profile_by_username(self, username: str) -> Optional[DiscoveredProfile]:
        return self._profiles_cache.get(username.lower().replace("@", ""))

# Global singleton session store
session_store = SessionStore()
