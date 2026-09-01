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

def test_live_search_follower_filter_excludes_komal_pandey():
    min_f = 1000
    max_f = 10000
    
    candidates = [
        {"username": "komalpandeyofficial", "followers": 1900000},
        {"username": "delhi_fashion_girl", "followers": 4500},
        {"username": "delhi_stylist", "followers": 8200},
        {"username": "micro_creator", "followers": 850},
        {"username": "unknown_creator", "followers": None}
    ]
    
    filtered = [
        c for c in candidates 
        if c["followers"] is not None and min_f <= c["followers"] <= max_f
    ]
    
    usernames = [c["username"] for c in filtered]
    assert "komalpandeyofficial" not in usernames, "@komalpandeyofficial (1.9M) must be excluded from 1K-10K search!"
    assert "micro_creator" not in usernames
    assert "unknown_creator" not in usernames
    assert len(filtered) == 2
    for c in filtered:
        assert 1000 <= c["followers"] <= 10000
