from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ConfidenceLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class ConfidenceDetail(BaseModel):
    field: str
    level: ConfidenceLevel
    source: str
    description: Optional[str] = None

class MatchReason(BaseModel):
    criterion: str
    matched: bool
    description: str
    score_contribution: float

class DiscoveredProfile(BaseModel):
    username: str
    profile_url: str
    display_name: Optional[str] = None
    bio: Optional[str] = None
    followers: Optional[int] = None
    followers_formatted: Optional[str] = "Not available"
    region: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    matched_keywords: List[str] = Field(default_factory=list)
    match_score: int = 0
    match_reasons: List[MatchReason] = Field(default_factory=list)
    data_confidence: ConfidenceLevel = ConfidenceLevel.LOW
    confidence_details: List[ConfidenceDetail] = Field(default_factory=list)
    is_demo: bool = False
    profile_image: Optional[str] = None
    following: Optional[int] = None
    posts: Optional[int] = None
    engagement_rate: Optional[float] = None
    category: Optional[str] = None
    discovery_source: str = "public_web_search"
    source_query: Optional[str] = None
