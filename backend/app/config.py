from pydantic import BaseModel

class ScoringWeights(BaseModel):
    niche_weight: float = 0.35
    region_weight: float = 0.25
    follower_weight: float = 0.20
    keyword_weight: float = 0.20

class Settings(BaseModel):
    app_name: str = "INSCOUT Engine"
    api_prefix: str = "/api"
    default_max_results: int = 30
    scoring_weights: ScoringWeights = ScoringWeights()
    # Demo data fallback strictly disabled
    enable_live_discovery_fallback: bool = False

settings = Settings()
