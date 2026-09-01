import sys
import time
import asyncio
import warnings

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding='utf-8')

from app.models.search import SearchRequest
from app.discovery.search_provider import SearchDiscoveryProvider

async def run_live_discovery_benchmarks():
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
            "name": "Delhi + Fashion (10K–100K)",
            "req": SearchRequest(
                region="Delhi",
                niche="Fashion",
                followers_min=10000,
                followers_max=100000,
                keywords=["stylist", "ootd"],
                provider="search",
                max_results=100
            )
        },
        {
            "id": "BENCHMARK 3",
            "name": "Mumbai + Travel (1K–10K)",
            "req": SearchRequest(
                region="Mumbai",
                niche="Travel",
                followers_min=1000,
                followers_max=10000,
                keywords=["traveler", "backpacker"],
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
        },
        {
            "id": "BENCHMARK 6",
            "name": "Delhi + Lifestyle (1K–50K)",
            "req": SearchRequest(
                region="Delhi",
                niche="Lifestyle",
                followers_min=1000,
                followers_max=50000,
                keywords=["vlog", "creator"],
                provider="search",
                max_results=100
            )
        }
    ]

    print("==========================================================================================", flush=True)
    print("INSCOUT LIVE DISCOVERY ENGINE — 6-SCENARIO FORENSIC BENCHMARK REPORT", flush=True)
    print("==========================================================================================", flush=True)

    summary_rows = []

    for test in test_scenarios:
        req = test["req"]
        
        start_time = time.perf_counter()
        data = await provider.discover_profiles_with_metrics(req)
        elapsed_sec = round(time.perf_counter() - start_time, 2)

        profiles = data["profiles"]
        c_disc = data["candidates_discovered"]
        u_cand = data["unique_candidates"]
        duplicates = max(0, c_disc - u_cand)
        p_ver = data["profiles_verified"]
        p_rej = data["profiles_rejected"]
        rej_breakdown = data["rejection_breakdown"]
        p_mat = data["profiles_matched"]
        p_ret = data["profiles_returned"]
        q_gen = data["queries_generated"]
        q_exec = data["queries_executed"]
        bias_pct = data["region_username_bias_pct"]
        evidence_pct = data["bio_location_evidence_pct"]

        # Follower range validation
        min_f = req.followers_min or 0
        max_f = req.followers_max or float('inf')
        for p in profiles:
            assert p.followers is not None, f"Profile @{p.username} has unknown follower count!"
            assert min_f <= p.followers <= max_f, f"Profile @{p.username} ({p.followers}) violates range {min_f}-{max_f}"

        row = {
            "id": test["id"],
            "name": test["name"],
            "q_gen": q_gen,
            "q_exec": q_exec,
            "c_disc": c_disc,
            "u_cand": u_cand,
            "duplicates": duplicates,
            "p_ver": p_ver,
            "f_rej": rej_breakdown.get("follower_out_of_range", 0) + rej_breakdown.get("follower_unknown", 0),
            "reg_rej": rej_breakdown.get("region_mismatch_or_unverified", 0),
            "niche_rej": rej_breakdown.get("niche_mismatch", 0),
            "p_mat": p_mat,
            "p_ret": p_ret,
            "bias_pct": bias_pct,
            "evidence_pct": evidence_pct,
            "duration": elapsed_sec
        }
        summary_rows.append(row)

        print(f"\n------------------------------------------------------------------------------------------", flush=True)
        print(f"[{test['id']}] {test['name']}", flush=True)
        print(f"  * Criteria: Region='{req.region}', Niche='{req.niche}', Followers={req.followers_min:,}–{req.followers_max:,}", flush=True)
        print(f"  * Queries Generated: {q_gen} | Queries Executed: {q_exec}", flush=True)
        print(f"  * Candidates: Discovered={c_disc} | Unique={u_cand} | Duplicates Removed={duplicates}", flush=True)
        print(f"  * Profiles Verified: {p_ver} | Total Rejected: {p_rej}", flush=True)
        print(f"  * Rejection Breakdown: Follower Range/Unknown={row['f_rej']}, Region Mismatch={row['reg_rej']}, Niche Mismatch={row['niche_rej']}", flush=True)
        print(f"  * Final Matches: {p_mat} | Displayed: {p_ret} (Time: {elapsed_sec}s)", flush=True)
        print(f"  * Quality Metrics: Region in Username Bias={bias_pct}% | Verified Bio Evidence={evidence_pct}%", flush=True)
        
        print(f"\n  Top Discovered Real Profiles (First {min(5, len(profiles))}):", flush=True)
        for idx, p in enumerate(profiles[:5], 1):
            f_str = f"{p.followers:,}" if p.followers else "Unknown"
            print(f"    {idx:2d}. @{p.username:<26} | Followers: {f_str:<10} | Region: {p.region or 'N/A':<10} | Score: {p.match_score}/100", flush=True)
            print(f"        URL: {p.profile_url}", flush=True)
            print(f"        Tags: {p.tags}", flush=True)
            print(f"        Bio: {p.bio}", flush=True)

    print("\n==========================================================================================", flush=True)
    print("FORENSIC BENCHMARK SUMMARY TABLE (6 SCENARIOS)", flush=True)
    print("==========================================================================================", flush=True)
    print(f"{'Benchmark':<13} | {'Criteria':<32} | {'Queries':<7} | {'Raw':<5} | {'Unique':<6} | {'Returned':<8} | {'Handle Bias %':<13} | {'Bio Evidence %':<14} | {'Time':<6}", flush=True)
    print("-" * 115, flush=True)
    for r in summary_rows:
        print(f"{r['id']:<13} | {r['name']:<32} | {r['q_gen']:<7} | {r['c_disc']:<5} | {r['u_cand']:<6} | {r['p_ret']:<8} | {r['bias_pct']:<13}% | {r['evidence_pct']:<14}% | {r['duration']:<6}s", flush=True)

if __name__ == "__main__":
    asyncio.run(run_live_discovery_benchmarks())
