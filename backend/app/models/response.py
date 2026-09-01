from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.profile import DiscoveredProfile
from app.models.search import SearchRequest

class SearchResponse(BaseModel):
    search_id: str
    query: SearchRequest
    total_found: int
    candidates_discovered: int = 0
    profiles_verified: int = 0
    profiles_matched: int = 0
    provider_used: str = "search"
    is_demo: bool = False
    profiles: List[DiscoveredProfile] = Field(default_factory=list)
    available_tags: List[str] = Field(default_factory=list)
    available_regions: List[str] = Field(default_factory=list)
    execution_time_ms: float = 0.0
    warning: Optional[str] = None

class ExportResponse(BaseModel):
    search_id: str
    filename: str
    csv_data: str
    row_count: int

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    active_providers: List[str]
