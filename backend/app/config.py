from pydantic import BaseModel

class ScoringWeights(BaseModel):
    niche_weight: float = 0.35
    region_weight: float = 0.25
    follower_weight: float = 0.20
    keyword_weight: float = 0.20

class DiscoverySettings(BaseModel):
    target_results: int = 100
    max_candidates: int = 500
    max_search_queries: int = 35
    search_batch_size: int = 5
    search_query_delay: float = 0.25

class Settings(BaseModel):
    app_name: str = "INSCOUT Engine V2"
    api_prefix: str = "/api"
    default_max_results: int = 100
    scoring_weights: ScoringWeights = ScoringWeights()
    discovery: DiscoverySettings = DiscoverySettings()
    enable_live_discovery_fallback: bool = False

settings = Settings()
