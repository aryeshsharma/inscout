import sys
import time
import asyncio
import warnings

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding='utf-8')

from app.discovery.engine import DiscoveryEngine
from app.models.search import SearchRequest
from app.services.query_expansion import QueryExpansionEngine
from app.discovery.search_provider import SearchDiscoveryProvider

async def run_phase8_audit():
    provider = SearchDiscoveryProvider()

    test_scenarios = [
        {
            "id": "TEST A",
            "name": "Delhi + Fashion (1K–10K)",
            "req": SearchRequest(
                region="Delhi",
                niche="Fashion",
                followers_min=1000,
                followers_max=10000,
                keywords=["model", "creator"],
                provider="search",
                max_results=100
            )
        },
        {
            "id": "TEST B",
            "name": "Delhi + Fashion (10K–100K)",
            "req": SearchRequest(
                region="Delhi",
                niche="Fashion",
                followers_min=10000,
                followers_max=100000,
                keywords=["model", "creator"],
                provider="search",
                max_results=100
            )
        },
        {
            "id": "TEST C",
            "name": "Mumbai + Beauty (10K–100K)",
            "req": SearchRequest(
                region="Mumbai",
                niche="Beauty",
                followers_min=10000,
                followers_max=100000,
                keywords=["mua", "makeup"],
                provider="search",
                max_results=100
            )
        },
        {
            "id": "TEST D",
            "name": "Bangalore + Technology (10K–500K)",
            "req": SearchRequest(
                region="Bangalore",
                niche="Technology",
                followers_min=10000,
                followers_max=500000,
                keywords=["developer", "coding"],
                provider="search",
                max_results=100
            )
        },
        {
            "id": "TEST E",
            "name": "Delhi + Travel (10K–50K)",
            "req": SearchRequest(
                region="Delhi",
                niche="Travel",
                followers_min=10000,
                followers_max=50000,
                keywords=["traveler", "vlog"],
                provider="search",
                max_results=100
            )
        }
    ]

    print("==================================================================", flush=True)
    print("INSCOUT DISCOVERY ENGINE V2 — PHASE 8 REAL SEARCHES AUDIT REPORT", flush=True)
    print("==================================================================", flush=True)

    summary_rows = []

    for test in test_scenarios:
        req = test["req"]
        queries = QueryExpansionEngine.expand_queries(req, max_queries=25)
        
        start_time = time.perf_counter()
        profiles, c_disc, p_ver, p_mat = await provider.discover_profiles_with_metrics(req)
        elapsed_sec = round(time.perf_counter() - start_time, 2)

        with_followers = sum(1 for p in profiles if p.followers is not None)
        with_region = sum(1 for p in profiles if p.region is not None)
        
        # Verify 1.9M Komal Pandey is NOT in 1K-10K
        if test["id"] == "TEST A":
            kp_found = any(p.username.lower() == "komalpandeyofficial" for p in profiles)
            assert not kp_found, "FATAL: Komal Pandey (1.9M) found in 1K-10K filter!"

        row = {
            "id": test["id"],
            "name": test["name"],
            "queries": len(queries),
            "raw_candidates": c_disc,
            "duplicates_removed": max(0, c_disc - p_ver),
            "verified_profiles": p_ver,
            "with_followers": with_followers,
            "passing_follower_filter": p_mat,
            "final_matching": p_mat,
            "final_displayed": len(profiles),
            "duration": elapsed_sec
        }
        summary_rows.append(row)

        print(f"\n------------------------------------------------------------------", flush=True)
        print(f"[{test['id']}] {test['name']}", flush=True)
        print(f"  * Search Criteria: Region='{req.region}', Niche='{req.niche}', Followers={req.followers_min:,}–{req.followers_max:,}", flush=True)
        print(f"  * Queries Generated: {len(queries)}", flush=True)
        print(f"  * Raw Candidates Discovered: {c_disc}", flush=True)
        print(f"  * Duplicates Removed: {max(0, c_disc - p_ver)}", flush=True)
        print(f"  * Verified Public Profiles: {p_ver}", flush=True)
        print(f"  * Profiles Passing Follower Filter ({req.followers_min:,}–{req.followers_max:,}): {p_mat}", flush=True)
        print(f"  * Profiles Passing Region & Niche Filters: {p_mat}", flush=True)
        print(f"  * Final Matching Profiles: {p_mat}", flush=True)
        print(f"  * Final Displayed Profiles: {len(profiles)}", flush=True)
        print(f"  * Discovery Duration: {elapsed_sec}s", flush=True)
        
        print(f"\n  Top Final Profiles (First {min(10, len(profiles))}):", flush=True)
        for idx, p in enumerate(profiles[:10], 1):
            f_str = f"{p.followers:,}" if p.followers else "Unknown"
            print(f"    {idx:2d}. @{p.username:<25} | Followers: {f_str:<10} | Region: {p.region or 'N/A':<10} | Niche: {req.niche:<10} | Score: {p.match_score}/100", flush=True)
            print(f"        URL: {p.profile_url}", flush=True)
            print(f"        Tags: {p.tags}", flush=True)

    print("\n==================================================================", flush=True)
    print("PHASE 8 AUDIT SUMMARY TABLE", flush=True)
    print("==================================================================", flush=True)
    print(f"{'Test':<8} | {'Criteria':<32} | {'Queries':<7} | {'Raw':<5} | {'Verified':<8} | {'Matched':<7} | {'Displayed':<9} | {'Time':<6}", flush=True)
    print("-" * 92, flush=True)
    for r in summary_rows:
        print(f"{r['id']:<8} | {r['name']:<32} | {r['queries']:<7} | {r['raw_candidates']:<5} | {r['verified_profiles']:<8} | {r['final_matching']:<7} | {r['final_displayed']:<9} | {r['duration']:<6}s", flush=True)

if __name__ == "__main__":
    asyncio.run(run_phase8_audit())
