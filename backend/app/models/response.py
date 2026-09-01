from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.profile import DiscoveredProfile
from app.models.search import SearchRequest

class SearchResponse(BaseModel):
    search_id: str
    query: SearchRequest
    total_found: int
    candidates_discovered: int = 0
    unique_candidates: int = 0
    profiles_verified: int = 0
    profiles_rejected: int = 0
    rejection_breakdown: Dict[str, int] = Field(default_factory=dict)
    follower_filter_passed: int = 0
    region_niche_passed: int = 0
    profiles_matched: int = 0
    profiles_returned: int = 0
    provider_used: str = "search"
    discovery_sources: List[str] = Field(default_factory=lambda: ["public_web_search"])
    queries_generated: int = 0
    queries_executed: int = 0
    pagination_used: bool = False
    region_username_bias_pct: float = 0.0
    bio_location_evidence_pct: float = 100.0
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
