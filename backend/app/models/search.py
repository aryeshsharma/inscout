from typing import List, Optional
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    region: Optional[str] = Field(default=None, description="Target city/region e.g., Delhi, Mumbai, Bangalore")
    niche: Optional[str] = Field(default=None, description="Primary niche e.g., Fashion, Tech, Fitness")
    followers_min: Optional[int] = Field(default=None, description="Minimum follower threshold")
    followers_max: Optional[int] = Field(default=None, description="Maximum follower threshold")
    keywords: List[str] = Field(default_factory=list, description="Target keywords e.g. model, styling, developer")
    provider: str = Field(default="auto", description="Discovery provider: 'auto', 'search', or 'mock'")
    max_results: int = Field(default=30, ge=1, le=100)

class SearchFilterParams(BaseModel):
    selected_tags: List[str] = Field(default_factory=list)
    selected_regions: List[str] = Field(default_factory=list)
    min_score: Optional[int] = Field(default=None, ge=0, le=100)
    followers_min: Optional[int] = None
    followers_max: Optional[int] = None
    sort_by: str = Field(default="score", description="score | followers | region | relevance")
    sort_order: str = Field(default="desc", description="asc | desc")
