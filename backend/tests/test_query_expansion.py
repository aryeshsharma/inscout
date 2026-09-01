from app.models.search import SearchRequest
from app.services.query_expansion import QueryExpansionEngine

def test_query_expansion_comprehensive():
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=10000,
        followers_max=100000,
        keywords=["model", "creator"],
        provider="search"
    )
    
    queries = QueryExpansionEngine.expand_queries(req, max_queries=30)
    assert len(queries) >= 15
    assert any("delhi" in q.lower() for q in queries)
    assert any("fashion" in q.lower() for q in queries)

def test_query_expansion_pan_india():
    req = SearchRequest(
        region="India",
        niche="Technology",
        followers_min=10000,
        followers_max=500000,
        keywords=["developer"],
        provider="search"
    )
    
    queries = QueryExpansionEngine.expand_queries(req, max_queries=20)
    assert len(queries) >= 10
    assert any("technology" in q.lower() or "developer" in q.lower() for q in queries)
