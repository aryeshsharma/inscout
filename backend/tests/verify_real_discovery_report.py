import sys
import time
import asyncio
import warnings

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding='utf-8')

from app.models.search import SearchRequest
from app.discovery.search_provider import SearchDiscoveryProvider

async def run_forensic_benchmarks():
    provider = SearchDiscoveryProvider()

    test_scenarios = [
        {
            "id": "BENCHMARK 1",
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
            "id": "BENCHMARK 2",
            "name": "Delhi + Travel (1K–10K)",
            "req": SearchRequest(
                region="Delhi",
                niche="Travel",
                followers_min=1000,
                followers_max=10000,
                keywords=["creator", "travel"],
                provider="search",
                max_results=100
            )
        },
        {
            "id": "BENCHMARK 3",
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
        },
        {
            "id": "BENCHMARK 4",
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
            "id": "BENCHMARK 5",
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
        }
    ]

    print("==================================================================================", flush=True)
    print("INSCOUT DISCOVERY ENGINE REDESIGN — FORENSIC BENCHMARK REPORT", flush=True)
    print("==================================================================================", flush=True)

    summary_rows = []

    for test in test_scenarios:
        req = test["req"]
        
        start_time = time.perf_counter()
        (
            profiles,
            c_disc,
            u_cand,
            p_ver,
            f_pass,
            rn_pass,
            q_gen,
            q_exec,
            pag_used
        ) = await provider.discover_profiles_with_metrics(req)
        elapsed_sec = round(time.perf_counter() - start_time, 2)

        # Verification: Komal Pandey must never be in 1K-10K
        if "1K–10K" in test["name"]:
            kp_found = any(p.username.lower() == "komalpandeyofficial" for p in profiles)
            assert not kp_found, "FATAL: Komal Pandey (1.9M) found in 1K-10K filter!"

        # Verification: Follower range must be strictly respected
        min_f = req.followers_min or 0
        max_f = req.followers_max or float('inf')
        for p in profiles:
            assert p.followers is not None, f"Profile {p.username} has unknown followers"
            assert min_f <= p.followers <= max_f, f"Profile @{p.username} ({p.followers}) violates range {min_f}-{max_f}"

        row = {
            "id": test["id"],
            "name": test["name"],
            "q_gen": q_gen,
            "q_exec": q_exec,
            "pag": "Yes" if pag_used else "No",
            "c_disc": c_disc,
            "u_cand": u_cand,
            "p_ver": p_ver,
            "f_pass": f_pass,
            "rn_pass": rn_pass,
            "returned": len(profiles),
            "duration": elapsed_sec
        }
        summary_rows.append(row)

        print(f"\n----------------------------------------------------------------------------------", flush=True)
        print(f"[{test['id']}] {test['name']}", flush=True)
        print(f"  * Search Criteria: Region='{req.region}', Niche='{req.niche}', Followers={req.followers_min:,}–{req.followers_max:,}", flush=True)
        print(f"  * Queries Generated: {q_gen} | Queries Executed: {q_exec} | Pagination: {'Yes' if pag_used else 'No'}", flush=True)
        print(f"  * Raw Candidates: {c_disc} | Unique Deduplicated: {u_cand} | Verified Profiles: {p_ver}", flush=True)
        print(f"  * Passed Follower Filter: {f_pass} | Passed Region & Niche Filters: {rn_pass}", flush=True)
        print(f"  * Final Returned Profiles: {len(profiles)} (Time: {elapsed_sec}s)", flush=True)
        
        print(f"\n  Inspected Profiles (Top {min(8, len(profiles))}):", flush=True)
        for idx, p in enumerate(profiles[:8], 1):
            f_str = f"{p.followers:,}" if p.followers else "Unknown"
            print(f"    {idx:2d}. @{p.username:<26} | Followers: {f_str:<10} | Region: {p.region or 'N/A':<10} | Score: {p.match_score}/100", flush=True)
            print(f"        URL: {p.profile_url}", flush=True)
            print(f"        Tags: {p.tags}", flush=True)

    print("\n==================================================================================", flush=True)
    print("FORENSIC BENCHMARK SUMMARY TABLE", flush=True)
    print("==================================================================================", flush=True)
    print(f"{'Benchmark':<13} | {'Criteria':<32} | {'Queries':<7} | {'Raw':<5} | {'Unique':<6} | {'Verified':<8} | {'Follower':<8} | {'Matched':<7} | {'Time':<6}", flush=True)
    print("-" * 105, flush=True)
    for r in summary_rows:
        print(f"{r['id']:<13} | {r['name']:<32} | {r['q_gen']:<7} | {r['c_disc']:<5} | {r['u_cand']:<6} | {r['p_ver']:<8} | {r['f_pass']:<8} | {r['returned']:<7} | {r['duration']:<6}s", flush=True)

if __name__ == "__main__":
    asyncio.run(run_forensic_benchmarks())
