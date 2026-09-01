from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.profile import DiscoveredProfile
from app.models.search import SearchRequest

class SearchResponse(BaseModel):
    search_id: str
    query: SearchRequest
    total_found: int
    provider_used: str
    is_demo: bool
    profiles: List[DiscoveredProfile]
    available_tags: List[str] = Field(default_factory=list)
    available_regions: List[str] = Field(default_factory=list)
    execution_time_ms: float
    warning: Optional[str] = None

class HealthResponse(BaseModel):
    status: str = "ok"
    app_name: str = "INSCOUT Engine"
    version: str = "1.0.0"
    active_providers: List[str] = ["mock", "search"]

class ExportResponse(BaseModel):
    search_id: str
    filename: str
    csv_data: str
    row_count: int
