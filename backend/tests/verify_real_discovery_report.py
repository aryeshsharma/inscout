import sys
import time
import asyncio
import warnings

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding='utf-8')

from app.discovery.engine import DiscoveryEngine
from app.models.search import SearchRequest
from app.services.query_expansion import QueryExpansionEngine

async def run_v2_audit():
    engine = DiscoveryEngine()

    test_scenarios = [
        {
            "id": 1,
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
            "id": 2,
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
            "id": 3,
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
            "id": 4,
            "name": "Delhi + Fitness (1K–50K)",
            "req": SearchRequest(
                region="Delhi",
                niche="Fitness",
                followers_min=1000,
                followers_max=50000,
                keywords=["trainer", "coach"],
                provider="search",
                max_results=100
            )
        },
        {
            "id": 5,
            "name": "India + Fashion (10K–100K)",
            "req": SearchRequest(
                region="India",
                niche="Fashion",
                followers_min=10000,
                followers_max=100000,
                keywords=["creator", "style"],
                provider="search",
                max_results=100
            )
        }
    ]

    print("==================================================================", flush=True)
    print("INSCOUT DISCOVERY ENGINE V2 — HIGH-VOLUME REAL PUBLIC DISCOVERY AUDIT", flush=True)
    print("==================================================================", flush=True)

    audit_summary = []

    for scenario in test_scenarios:
        req = scenario["req"]
        queries = QueryExpansionEngine.expand_queries(req, max_queries=25)
        
        print(f"\nRunning Scenario {scenario['id']}: {scenario['name']}...", flush=True)
        start_time = time.perf_counter()
        profiles, provider_used, is_demo, warning, c_disc, p_ver, p_mat = await engine.execute_discovery(req)
        elapsed_sec = round(time.perf_counter() - start_time, 2)

        with_followers = sum(1 for p in profiles if p.followers is not None)
        with_location = sum(1 for p in profiles if p.region is not None)
        strong_matches = sum(1 for p in profiles if p.match_score >= 60)
        
        report_row = {
            "name": scenario["name"],
            "queries_generated": len(queries),
            "candidates_discovered": c_disc,
            "duplicates_filtered": max(0, c_disc - p_ver),
            "profiles_verified": p_ver,
            "profiles_matched": len(profiles),
            "with_followers": with_followers,
            "with_location": with_location,
            "strong_matches": strong_matches,
            "target_reached": len(profiles) >= 100,
            "discovery_time_sec": elapsed_sec,
            "is_demo": is_demo
        }
        audit_summary.append(report_row)

        print(f"------------------------------------------------------------------", flush=True)
        print(f"SCENARIO {scenario['id']}: {scenario['name']}", flush=True)
        print(f" * Search Queries Generated: {len(queries)}", flush=True)
        print(f" * Raw Candidates Discovered: {c_disc}", flush=True)
        print(f" * Unique Profiles Verified: {p_ver}", flush=True)
        print(f" * Discovered Public Profiles: {len(profiles)}", flush=True)
        print(f" * Profiles with Indexed Followers: {with_followers}", flush=True)
        print(f" * Profiles with Regional Signals: {with_location}", flush=True)
        print(f" * Target (100) Reached: {'YES' if len(profiles) >= 100 else f'NO (Truthful yield: {len(profiles)})'}", flush=True)
        print(f" * Discovery Duration: {elapsed_sec}s | Is Demo: {is_demo}", flush=True)
        
        print("\n Top 5 Ranked Discovered Profiles:", flush=True)
        for idx, p in enumerate(profiles[:5], 1):
            f_display = p.followers_formatted if p.followers_formatted else "Not available"
            reg_display = p.region or "Not available"
            print(f"   {idx}. @{p.username:<25} | Followers: {f_display:<12} | Region: {reg_display:<10} | Score: {p.match_score}/100", flush=True)
            print(f"      URL: {p.profile_url}", flush=True)
            print(f"      Tags: {p.tags}", flush=True)

    print("\n==================================================================", flush=True)
    print("V2 AUDIT SUMMARY TABLE (Section 25 Requirements)", flush=True)
    print("==================================================================", flush=True)
    print(f"{'Scenario':<32} | {'Queries':<7} | {'Candidates':<10} | {'Verified':<8} | {'Yield':<6} | {'Followers':<9} | {'Time (s)':<8}", flush=True)
    print("-" * 90, flush=True)
    for r in audit_summary:
        print(f"{r['name']:<32} | {r['queries_generated']:<7} | {r['candidates_discovered']:<10} | {r['profiles_verified']:<8} | {r['profiles_matched']:<6} | {r['with_followers']:<9} | {r['discovery_time_sec']:<8}", flush=True)

if __name__ == "__main__":
    asyncio.run(run_v2_audit())
