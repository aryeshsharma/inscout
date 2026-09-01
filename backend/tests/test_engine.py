import pytest
from app.models.search import SearchRequest
from app.models.profile import ConfidenceLevel
from app.services.scorer import ScoringEngine
from app.services.tagger import TaggingEngine
from app.services.query_generator import QueryGenerator
from app.services.query_expansion import QueryExpansionEngine
from app.services.normalizer import ProfileNormalizer
from app.discovery.engine import DiscoveryEngine
from app.discovery.mock_provider import MockDiscoveryProvider

def test_query_generator_and_expansion():
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        keywords=["model", "creator"],
        followers_min=10000,
        followers_max=50000
    )
    dork = QueryGenerator.generate_dork_query(req)
    assert "site:instagram.com" in dork
    assert '"Delhi"' in dork
    assert '"Fashion"' in dork

    expanded = QueryExpansionEngine.expand_queries(req, max_queries=30)
    assert len(expanded) >= 20
    assert any("fashion" in q.lower() for q in expanded)
    assert any("delhi" in q.lower() for q in expanded)

def test_tagging_engine():
    bio = "Delhi NCR | Fashion & Lifestyle Creator | Model | DM for collaborations & PR"
    tags = TaggingEngine.extract_tags(bio, user_query_niche="Fashion")
    assert "Fashion" in tags
    assert "Lifestyle" in tags
    assert "Model" in tags
    assert "Open for Collabs" in tags

    region = TaggingEngine.detect_region(bio)
    assert region == "Delhi"

def test_normalizer():
    assert ProfileNormalizer.extract_username_from_url("https://www.instagram.com/tanya.style/") == "tanya.style"
    assert ProfileNormalizer.extract_username_from_url("https://www.instagram.com/explore/") is None
    assert ProfileNormalizer.extract_username_from_url("https://www.instagram.com/popular/") is None
    
    assert ProfileNormalizer.parse_follower_count("42.5K Followers, 500 Following") == 42500
    assert ProfileNormalizer.parse_follower_count("1.2M followers") == 1200000
    assert ProfileNormalizer.parse_follower_count("50,000 Followers") == 50000

    assert ProfileNormalizer.format_followers(42300) == "42.3K"
    assert ProfileNormalizer.format_followers(None) == "Not available"

def test_scoring_engine():
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=10000,
        followers_max=50000,
        keywords=["model", "creator"]
    )
    
    score, reasons, matched_kws = ScoringEngine.calculate_match_score(
        bio="Based in New Delhi | Fashion Creator | Model | Collabs",
        display_name="Tanya",
        tags=["Fashion", "Model", "Open for Collabs"],
        region="Delhi",
        region_confidence="HIGH",
        data_confidence=ConfidenceLevel.HIGH,
        request=req
    )
    
    assert 85 <= score <= 100
    assert len(reasons) >= 4 # Niche, Region, Keywords, Context, Confidence
    assert any("Fashion niche" in r.description for r in reasons)
    assert any("Delhi" in r.description for r in reasons)
    assert any("model" in k.lower() or "creator" in k.lower() for k in matched_kws)

@pytest.mark.asyncio
async def test_mock_discovery_provider_isolated():
    provider = MockDiscoveryProvider()
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=10000,
        followers_max=100000,
        keywords=["model"]
    )
    profiles = await provider.discover_profiles(req)
    assert len(profiles) > 0
    top_profile = profiles[0]
    assert top_profile.is_demo is True
    assert top_profile.match_score > 70
    assert "Fashion" in top_profile.tags

def test_discovery_engine_v2():
    engine = DiscoveryEngine()
    provider = engine.get_provider("search")
    assert provider.provider_name == "search"
    assert provider.is_demo is False
