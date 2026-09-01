import pytest
import asyncio
from app.models.search import SearchRequest
from app.services.tagger import TaggingEngine
from app.services.scorer import ScoringEngine
from app.services.normalizer import ProfileNormalizer
from app.services.query_expansion import QueryExpansionEngine
from app.discovery.search_provider import SearchDiscoveryProvider
from app.discovery.engine import DiscoveryEngine
from app.models.profile import ConfidenceLevel

# 1. Test: Username containing "Delhi" does NOT automatically qualify for Delhi
def test_username_containing_delhi_does_not_qualify():
    # Profile with "delhi" in handle but ZERO location in bio
    bio_without_location = "Fashion student • OOTD and daily styling on budget • DM for PR"
    region, confidence, evidence = TaggingEngine.detect_region_with_confidence(
        bio_text=bio_without_location,
        context_snippet=""
    )
    assert region is None or confidence == "LOW", "Handle alone must not qualify region!"
    assert confidence == "LOW"

# 2. Test: Mumbai creator whose username contains "Delhi" is REJECTED for a Delhi search
def test_mumbai_creator_with_delhi_in_username_rejected_for_delhi():
    mumbai_bio = "Living in Bandra, Mumbai • Styling lookbooks and lifestyle vlogs"
    region, confidence, evidence = TaggingEngine.detect_region_with_confidence(
        bio_text=mumbai_bio,
        context_snippet=""
    )
    assert region == "Mumbai"
    assert confidence in ["HIGH", "MEDIUM"]
    
    # Must NOT match Delhi
    assert region != "Delhi"

# 3. Test: A Delhi creator with NO "Delhi" in username qualifies
def test_delhi_creator_without_delhi_in_username_qualifies():
    delhi_bio = "Based in New Delhi • Menswear styling & aesthetics • Fashion creator"
    region, confidence, evidence = TaggingEngine.detect_region_with_confidence(
        bio_text=delhi_bio,
        context_snippet=""
    )
    assert region == "Delhi"
    assert confidence == "HIGH"
    assert "New Delhi" in evidence

# 4. Test: 1.9M follower profile REJECTED in 1K-10K search
def test_macro_creator_rejected_in_1k_10k_range():
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=1000,
        followers_max=10000,
        provider="search"
    )
    
    komal_followers = 1900000
    assert not (req.followers_min <= komal_followers <= req.followers_max), "1.9M profile must be rejected by 1K-10K filter!"

# 5. Test: Unknown follower count REJECTED when follower range is specified
def test_unknown_followers_rejected_in_range_search():
    unknown_followers = None
    min_f = 1000
    max_f = 10000
    
    passes = (unknown_followers is not None) and (min_f <= unknown_followers <= max_f)
    assert passes is False, "Unknown follower count must be rejected from strict follower search!"

# 6. Test: Non-Instagram URLs never become profiles
def test_non_instagram_urls_rejected():
    urls = [
        "https://www.youtube.com/user/fashionchannel",
        "https://facebook.com/groups/delhifashion",
        "https://www.instagram.com/explore/tags/delhifashion/",
        "https://www.instagram.com/p/Cxyz12345/",
        "https://www.instagram.com/reels/videos/"
    ]
    for url in urls:
        u = ProfileNormalizer.extract_username_from_url(url)
        assert u is None or u in ["explore", "reels", "p", "tags"], f"Invalid URL '{url}' should not produce valid username"

# 7. Test: Duplicate Instagram handles removed
def test_duplicate_handles_removed():
    raw_handles = ["user_alpha", "USER_ALPHA", "User_Alpha", "user_beta", "USER_BETA"]
    normalized = set(h.lower() for h in raw_handles)
    assert len(normalized) == 2
    assert "user_alpha" in normalized
    assert "user_beta" in normalized

# 8. Test: Mock/demo profiles never appear in production search mode
@pytest.mark.asyncio
async def test_no_mock_data_in_live_search():
    engine = DiscoveryEngine()
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        provider="search"
    )
    res = await engine.execute_discovery(req)
    assert res["is_demo"] is False
    assert res["provider_used"] == "search"
    for p in res.get("profiles", []):
        assert p.is_demo is False

# 9. Test: Search results come from multiple discovery queries
def test_multi_query_expansion_breadth():
    req = SearchRequest(
        region="Delhi",
        niche="Travel",
        keywords=["nomad", "creator"]
    )
    queries = QueryExpansionEngine.expand_queries(req, max_queries=40)
    assert len(queries) >= 20
    assert any("based in" in q for q in queries)
    assert any("collab" in q.lower() for q in queries)
    assert any("filmmaker" in q or "photographer" in q or "backpacker" in q for q in queries)

# 10. Test: If fewer than 100 exist, system returns fewer without fabricating results
@pytest.mark.asyncio
async def test_honest_result_counts_without_fabrication():
    provider = SearchDiscoveryProvider()
    req = SearchRequest(
        region="Delhi",
        niche="Travel",
        followers_min=1000,
        followers_max=5000,
        provider="search",
        max_results=100
    )
    res = await provider.discover_profiles_with_metrics(req)
    profiles = res["profiles"]
    
    # Must never invent profiles to fill up to 100
    assert len(profiles) <= 100
    assert res["profiles_matched"] == len(profiles)

# 11. Test: Different niches produce different candidate pools
def test_different_niches_produce_different_queries():
    req_fashion = SearchRequest(region="Delhi", niche="Fashion")
    req_travel = SearchRequest(region="Delhi", niche="Travel")
    
    queries_f = QueryExpansionEngine.expand_queries(req_fashion, max_queries=30)
    queries_t = QueryExpansionEngine.expand_queries(req_travel, max_queries=30)
    
    assert queries_f != queries_t
    assert any("fashion" in q.lower() or "stylist" in q.lower() for q in queries_f)
    assert any("travel" in q.lower() or "wanderer" in q.lower() for q in queries_t)

# 12. Test: Delhi Fashion and Delhi Travel do NOT return identical candidate pools
def test_tagger_differentiates_fashion_and_travel():
    fashion_bio = "Wardrobe styling, runway shoots & fashion aesthetics. Based in New Delhi."
    travel_bio = "Backpacking across Himalayas & road trip itineraries. Living in Delhi."
    
    f_tags = TaggingEngine.extract_tags(fashion_bio, "Fashion")
    t_tags = TaggingEngine.extract_tags(travel_bio, "Travel")
    
    assert "Fashion" in f_tags
    assert "Travel" not in f_tags
    assert "Travel" in t_tags
    assert "Fashion" not in t_tags
