import time
import uuid
from typing import List, Set, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.search import SearchRequest
from app.models.response import SearchResponse, HealthResponse, ExportResponse
from app.models.profile import DiscoveredProfile
from app.discovery.engine import DiscoveryEngine
from app.services.exporter import Exporter
from app.storage.session_store import session_store

app = FastAPI(
    title=settings.app_name,
    description="High-Volume Real Public Instagram Profile Discovery & Filtering Engine API (V3.0)",
    version="3.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

discovery_engine = DiscoveryEngine()

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version="3.0.0",
        active_providers=["search", "meta_business_discovery"]
    )

@app.post("/api/search", response_model=SearchResponse)
async def execute_search(request: SearchRequest):
    start_time = time.perf_counter()
    search_id = str(uuid.uuid4())
    
    discovery_data = await discovery_engine.execute_discovery(request)
    profiles = discovery_data.get("profiles", [])
    
    # Collect unique available tags and regions across results for quick filtering
    tags_set: Set[str] = set()
    regions_set: Set[str] = set()
    
    for p in profiles:
        for t in p.tags:
            tags_set.add(t)
        if p.region:
            regions_set.add(p.region)
            
    execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    response = SearchResponse(
        search_id=search_id,
        query=request,
        total_found=len(profiles),
        candidates_discovered=discovery_data.get("candidates_discovered", 0),
        unique_candidates=discovery_data.get("unique_candidates", 0),
        profiles_verified=discovery_data.get("profiles_verified", 0),
        profiles_rejected=discovery_data.get("profiles_rejected", 0),
        rejection_breakdown=discovery_data.get("rejection_breakdown", {}),
        follower_filter_passed=discovery_data.get("follower_filter_passed", 0),
        region_niche_passed=discovery_data.get("region_niche_passed", 0),
        profiles_matched=discovery_data.get("profiles_matched", len(profiles)),
        profiles_returned=discovery_data.get("profiles_returned", len(profiles)),
        provider_used=discovery_data.get("provider_used", "search"),
        discovery_sources=discovery_data.get("discovery_sources", ["public_web_search"]),
        queries_generated=discovery_data.get("queries_generated", 0),
        queries_executed=discovery_data.get("queries_executed", 0),
        pagination_used=discovery_data.get("pagination_used", False),
        region_username_bias_pct=discovery_data.get("region_username_bias_pct", 0.0),
        bio_location_evidence_pct=discovery_data.get("bio_location_evidence_pct", 100.0),
        is_demo=discovery_data.get("is_demo", False),
        profiles=profiles,
        available_tags=sorted(list(tags_set)),
        available_regions=sorted(list(regions_set)),
        execution_time_ms=execution_time_ms,
        warning=discovery_data.get("warning")
    )
    
    session_store.save_search(search_id, response)
    return response

@app.get("/api/results/{search_id}", response_model=SearchResponse)
async def get_results(search_id: str):
    search_res = session_store.get_search(search_id)
    if not search_res:
        raise HTTPException(status_code=404, detail="Search session expired or not found")
    return search_res

@app.get("/api/debug/search/{search_id}")
async def get_search_debug_audit(search_id: str):
    """
    Provenance & Audit Debug Endpoint.
    Returns detailed audit telemetry for every profile in the search session.
    """
    search_res = session_store.get_search(search_id)
    if not search_res:
        raise HTTPException(status_code=404, detail="Search session not found")
        
    provenance_list = []
    for p in search_res.profiles:
        provenance_list.append({
            "username": p.username,
            "profile_url": p.profile_url,
            "followers": p.followers,
            "follower_status": p.follower_status,
            "region": p.region,
            "tags": p.tags,
            "match_score": p.match_score,
            "match_reasons": [r.dict() for r in p.match_reasons],
            "data_confidence": p.data_confidence,
            "source_query": p.source_query,
            "discovery_source": p.discovery_source
        })
        
    return {
        "search_id": search_id,
        "query": search_res.query.dict(),
        "candidates_discovered": search_res.candidates_discovered,
        "unique_candidates": search_res.unique_candidates,
        "profiles_verified": search_res.profiles_verified,
        "profiles_rejected": search_res.profiles_rejected,
        "rejection_breakdown": search_res.rejection_breakdown,
        "region_username_bias_pct": search_res.region_username_bias_pct,
        "bio_location_evidence_pct": search_res.bio_location_evidence_pct,
        "total_returned": search_res.total_found,
        "provenance": provenance_list
    }

@app.get("/api/profile/{username}", response_model=DiscoveredProfile)
async def get_profile(username: str):
    profile = session_store.get_profile_by_username(username)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile @{username} not found in recent search cache")
    return profile

@app.get("/api/export/{search_id}")
async def export_results(search_id: str, format: str = Query(default="csv", pattern="^(csv|json)$")):
    search_res = session_store.get_search(search_id)
    if not search_res:
        raise HTTPException(status_code=404, detail="Search session expired or not found")
        
    csv_content = Exporter.export_to_csv(search_res.profiles)
    filename = f"inscout_export_{search_res.query.niche or 'profiles'}_{search_id[:8]}.csv"
    
    if format == "json":
        return ExportResponse(
            search_id=search_id,
            filename=filename,
            csv_data=csv_content,
            row_count=len(search_res.profiles)
        )
        
    return Response(
        content=csv_content.encode("utf-8-sig"),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
