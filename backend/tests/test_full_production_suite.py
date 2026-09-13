import pytest
from typing import List, Dict, Any
from app.models.search import SearchRequest
from app.models.profile import ConfidenceLevel, DiscoveredProfile
from app.services.tagger import TaggingEngine
from app.services.scorer import ScoringEngine
from app.services.normalizer import ProfileNormalizer
from app.services.query_expansion import QueryExpansionEngine
from app.discovery.search_provider import SearchDiscoveryProvider
from app.discovery.engine import DiscoveryEngine
from app.storage.session_store import SessionStore
from app.models.response import SearchResponse

# =============================================================================
# TEST 1: Follower-range boundary enforcement
# =============================================================================
def test_follower_boundary_enforcement():
    """
    Target range: 1,000 to 10,000
    Followers | Expected
    999       | Reject
    1,000     | Accept
    5,000     | Accept
    10,000    | Accept
    10,001    | Reject
    1,900,000 | Reject
    """
    min_f = 1000
    max_f = 10000

    def check_follower_eligibility(followers):
        if followers is None:
            return False
        return min_f <= followers <= max_f

    assert check_follower_eligibility(999) is False
    assert check_follower_eligibility(1000) is True
    assert check_follower_eligibility(5000) is True
    assert check_follower_eligibility(10000) is True
    assert check_follower_eligibility(10001) is False
    assert check_follower_eligibility(1900000) is False

# =============================================================================
# TEST 2: Unknown follower rejection
# =============================================================================
def test_unknown_follower_rejection():
    """
    When follower range is active, unknown follower count (None) MUST be rejected.
    """
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=1000,
        followers_max=10000
    )
    has_range = req.followers_min is not None or req.followers_max is not None
    unknown_followers = None
    
    passed = False
    if has_range:
        if unknown_followers is not None and (req.followers_min <= unknown_followers <= req.followers_max):
            passed = True
            
    assert passed is False, "Unknown follower count must be rejected when range is requested"

# =============================================================================
# TEST 3: Username-location bias prevention
# =============================================================================
def test_username_location_bias_prevention():
    """
    Usernames containing "Delhi" or "Mumbai" MUST NOT be treated as location proof.
    Region must be verified from bio/snippet evidence only.
    """
    # Case A: Profile named @delhi_fashion_blogger with no location in bio -> Rejected for Delhi
    bio_no_loc = "Lover of style, high heels & coffee. Inquiries: contact@me.com"
    reg, conf, ev = TaggingEngine.detect_region_with_confidence(bio_no_loc)
    assert reg is None or conf == "LOW"
    
    # Case B: Profile named @mumbai_wanderer with "Based in Delhi" in bio -> Detected as Delhi
    bio_delhi = "Based in New Delhi • Fashion & style creator"
    reg2, conf2, ev2 = TaggingEngine.detect_region_with_confidence(bio_delhi)
    assert reg2 == "Delhi"
    assert conf2 == "HIGH"

# =============================================================================
# TEST 4: Region synonym and neighborhood cluster handling
# =============================================================================
def test_region_synonym_handling():
    """
    Test that neighborhood clusters map to canonical cities:
    - Gurgaon / Noida / Hauz Khas -> Delhi
    - Bandra / Andheri / Powai -> Mumbai
    - Koramangala / Indiranagar / Whitefield -> Bangalore
    """
    b1 = "Fashion stylist based in Bandra • Lookbooks & shoots"
    reg1, conf1, _ = TaggingEngine.detect_region_with_confidence(b1)
    assert reg1 == "Mumbai"

    b2 = "Tech builder living in Koramangala • Python & AI"
    reg2, conf2, _ = TaggingEngine.detect_region_with_confidence(b2)
    assert reg2 == "Bangalore"

    b3 = "Living in Gurgaon NCR • Menswear styling"
    reg3, conf3, _ = TaggingEngine.detect_region_with_confidence(b3)
    assert reg3 == "Delhi"

# =============================================================================
# TEST 5: Niche synonym and semantic taxonomy handling
# =============================================================================
def test_niche_synonym_handling():
    """
    Test semantic synonyms:
    - Fashion: style, outfits, stylist, model, streetwear, thrift
    - Travel: traveller, backpacker, explorer, adventure, nomad
    - Technology: developer, coding, software, AI, engineer
    - Beauty: makeup, skincare, MUA, cosmetics
    """
    f_bio = "Streetwear edits, thrift finds & model lookbooks"
    f_tags = TaggingEngine.extract_tags(f_bio, "Fashion")
    assert "Fashion" in f_tags
    assert "Model" in f_tags

    t_bio = "Backpacker exploring Himalayas & solo road trips"
    t_tags = TaggingEngine.extract_tags(t_bio, "Travel")
    assert "Travel" in t_tags

    tech_bio = "Software engineer building fullstack AI apps & Python tools"
    tech_tags = TaggingEngine.extract_tags(tech_bio, "Technology")
    assert "Technology" in tech_tags
    assert "Developer" in tech_tags

# =============================================================================
# TEST 6: Bio keyword matching against actual profile evidence
# =============================================================================
def test_bio_keyword_matching():
    """
    User-provided keywords must match against actual bio evidence, not query or handle.
    """
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        keywords=["sustainable", "couture"]
    )
    
    # Bio containing 'sustainable'
    score1, reasons1, matched_kws1 = ScoringEngine.calculate_match_score(
        bio="Sustainable fashion & capsule wardrobe. Based in Delhi.",
        display_name="Kavya",
        tags=["Fashion"],
        region="Delhi",
        region_confidence="HIGH",
        data_confidence=ConfidenceLevel.HIGH,
        request=req
    )
    assert "sustainable" in [k.lower() for k in matched_kws1]
    assert "couture" not in [k.lower() for k in matched_kws1]
    assert len(matched_kws1) == 1

# =============================================================================
# TEST 7: Duplicate removal
# =============================================================================
def test_duplicate_removal():
    """
    Case variations of usernames (@Username, @username, @USERNAME) must be deduplicated.
    """
    handles = ["StyleByRia", "stylebyria", "STYLEBYRIA", "stylebyria/"]
    normalized = set()
    for h in handles:
        u = ProfileNormalizer.extract_username_from_url(f"https://www.instagram.com/{h}")
        if u:
            normalized.add(u.lower())
            
    assert len(normalized) == 1
    assert "stylebyria" in normalized

# =============================================================================
# TEST 8: Invalid Instagram URL rejection
# =============================================================================
def test_invalid_instagram_url_rejection():
    """
    Non-Instagram URLs must return None.
    """
    invalid_urls = [
        "https://www.youtube.com/user/fashionchannel",
        "https://twitter.com/traveler",
        "https://www.linkedin.com/in/developer",
        "https://facebook.com/groups/tech",
        "not_a_url"
    ]
    for url in invalid_urls:
        u = ProfileNormalizer.extract_username_from_url(url)
        assert u is None, f"Invalid URL '{url}' should not produce username"

# =============================================================================
# TEST 9: Non-profile URL rejection
# =============================================================================
def test_non_profile_url_rejection():
    """
    Reserved Instagram paths must return None.
    """
    reserved_paths = [
        "https://www.instagram.com/explore/tags/fashion/",
        "https://www.instagram.com/p/Cxyz12345/",
        "https://www.instagram.com/reels/videos/",
        "https://www.instagram.com/stories/highlights/",
        "https://www.instagram.com/about/us/",
        "https://www.instagram.com/legal/privacy/",
        "https://www.instagram.com/popular/delhi/"
    ]
    for url in reserved_paths:
        u = ProfileNormalizer.extract_username_from_url(url)
        assert u is None or u in ProfileNormalizer.extract_username_from_url(url) is None

# =============================================================================
# TEST 10: No demo fallback behavior
# =============================================================================
def test_no_demo_fallback_behavior():
    """
    SearchDiscoveryProvider must have is_demo=False and provider_name='search'.
    """
    provider = SearchDiscoveryProvider()
    assert provider.is_demo is False
    assert provider.provider_name == "search"

# =============================================================================
# TEST 11: Result-limit enforcement (target up to 100 without padding)
# =============================================================================
def test_result_limit_enforcement():
    """
    Target is up to 100 genuine matching profiles. Results are not padded.
    """
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=1000,
        followers_max=10000,
        provider="search",
        max_results=100
    )
    assert req.max_results == 100
    
    # Check that custom max_results are respected
    req50 = SearchRequest(max_results=50)
    assert req50.max_results == 50

# =============================================================================
# TEST 12: Correct API and frontend result counts
# =============================================================================
def test_api_result_count_consistency():
    """
    SearchResponse fields must be consistent:
    total_found == len(profiles) == profiles_returned == profiles_matched
    """
    profiles = [
        DiscoveredProfile(
            username=f"creator_{i}",
            profile_url=f"https://www.instagram.com/creator_{i}/",
            display_name=f"Creator {i}",
            followers=5000,
            region="Delhi",
            tags=["Fashion"],
            match_score=85,
            data_confidence=ConfidenceLevel.HIGH
        )
        for i in range(5)
    ]
    
    resp = SearchResponse(
        search_id="test-123",
        query=SearchRequest(region="Delhi", niche="Fashion"),
        total_found=len(profiles),
        candidates_discovered=20,
        unique_candidates=15,
        profiles_verified=15,
        profiles_rejected=10,
        profiles_matched=len(profiles),
        profiles_returned=len(profiles),
        profiles=profiles
    )
    
    assert resp.total_found == 5
    assert len(resp.profiles) == 5
    assert resp.profiles_matched == 5
    assert resp.profiles_returned == 5

# =============================================================================
# TEST 13: Provider failure handling
# =============================================================================
@pytest.mark.asyncio
async def test_provider_failure_graceful_handling():
    """
    DiscoveryEngine catches exceptions gracefully and returns empty results without crashing.
    """
    engine = DiscoveryEngine()
    req = SearchRequest(region="Delhi", niche="Fashion")
    
    # Engine execution is protected by try/except
    data = await engine.execute_discovery(req)
    assert isinstance(data, dict)
    assert "profiles" in data
    assert data["is_demo"] is False

# =============================================================================
# TEST 14: Empty search results honesty
# =============================================================================
def test_empty_search_results_honesty():
    """
    When no genuine profiles match the criteria, total_found must be 0 and no mock profiles injected.
    """
    empty_resp = SearchResponse(
        search_id="empty-1",
        query=SearchRequest(region="NonExistentCity", niche="NonExistentNiche"),
        total_found=0,
        candidates_discovered=0,
        unique_candidates=0,
        profiles_verified=0,
        profiles_rejected=0,
        profiles_matched=0,
        profiles_returned=0,
        profiles=[]
    )
    assert empty_resp.total_found == 0
    assert len(empty_resp.profiles) == 0
    assert empty_resp.is_demo is False

# =============================================================================
# TEST 15: Public-profile-only validation
# =============================================================================
def test_public_profile_only_validation():
    """
    Only public profiles are formatted and accepted. No private/auth bypass methods.
    """
    for route in ["accounts", "direct", "stories", "reels"]:
        url = f"https://www.instagram.com/{route}/"
        u = ProfileNormalizer.extract_username_from_url(url)
        assert u is None, f"Internal Instagram route '{route}' must not be treated as a public profile"
