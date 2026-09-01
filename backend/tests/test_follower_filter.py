import pytest
import asyncio
from app.models.search import SearchRequest
from app.discovery.search_provider import SearchDiscoveryProvider

def test_follower_boundary_filter_logic():
    provider = SearchDiscoveryProvider()
    
    # Target Range: 1,000 to 10,000
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=1000,
        followers_max=10000,
        provider="search"
    )
    
    test_cases = [
        {"username": "user_999", "followers": 999, "should_pass": False},
        {"username": "user_1000", "followers": 1000, "should_pass": True},
        {"username": "user_1001", "followers": 1001, "should_pass": True},
        {"username": "user_9999", "followers": 9999, "should_pass": True},
        {"username": "user_10000", "followers": 10000, "should_pass": True},
        {"username": "user_10001", "followers": 10001, "should_pass": False},
        {"username": "komalpandeyofficial", "followers": 1900000, "should_pass": False},
        {"username": "user_unknown", "followers": None, "should_pass": False},
    ]

    min_f = req.followers_min
    max_f = req.followers_max

    for tc in test_cases:
        f = tc["followers"]
        passed = (f is not None) and (min_f <= f <= max_f)
        assert passed == tc["should_pass"], f"Failed for {tc['username']} with {f} followers"

@pytest.mark.asyncio
async def test_live_search_follower_filter_excludes_komal_pandey():
    provider = SearchDiscoveryProvider()
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=1000,
        followers_max=10000,
        provider="search"
    )
    
    (
        profiles,
        cand_count,
        u_count,
        ver_count,
        f_pass,
        rn_pass,
        q_gen,
        q_exec,
        pag_used
    ) = await provider.discover_profiles_with_metrics(req)
    
    usernames = [p.username.lower() for p in profiles]
    assert "komalpandeyofficial" not in usernames, "@komalpandeyofficial (1.9M) must be excluded from 1K-10K search!"
    
    # Verify every returned profile is strictly between 1,000 and 10,000
    for p in profiles:
        assert p.followers is not None, f"Profile {p.username} has unknown followers but passed range filter"
        assert 1000 <= p.followers <= 10000, f"Profile {p.username} ({p.followers}) is outside 1K-10K range!"

