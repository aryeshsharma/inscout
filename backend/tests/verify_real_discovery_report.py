import sys
import httpx
from app.discovery.engine import DiscoveryEngine
from app.models.search import SearchRequest

sys.stdout.reconfigure(encoding='utf-8')

async def run_live_audit():
    engine = DiscoveryEngine()

    test_scenarios = [
        {
            "id": 1,
            "name": "Delhi + Fashion",
            "req": SearchRequest(
                region="Delhi",
                niche="Fashion",
                followers_min=10000,
                followers_max=100000,
                keywords=["model", "creator"],
                provider="search"
            )
        },
        {
            "id": 2,
            "name": "Mumbai + Beauty",
            "req": SearchRequest(
                region="Mumbai",
                niche="Beauty",
                followers_min=10000,
                followers_max=200000,
                keywords=["mua", "makeup"],
                provider="search"
            )
        },
        {
            "id": 3,
            "name": "Bangalore + Technology",
            "req": SearchRequest(
                region="Bangalore",
                niche="Technology",
                followers_min=5000,
                followers_max=500000,
                keywords=["developer", "coding"],
                provider="search"
            )
        },
        {
            "id": 4,
            "name": "Delhi + Fitness",
            "req": SearchRequest(
                region="Delhi",
                niche="Fitness",
                followers_min=1000,
                followers_max=100000,
                keywords=["trainer", "coach"],
                provider="search"
            )
        },
        {
            "id": 5,
            "name": "India + Fashion",
            "req": SearchRequest(
                region="India",
                niche="Fashion",
                followers_min=10000,
                followers_max=500000,
                keywords=["creator", "style"],
                provider="search"
            )
        }
    ]

    print("==================================================================")
    print("INSCOUT — REAL PUBLIC INSTAGRAM PROFILE DISCOVERY AUDIT")
    print("==================================================================")

    for scenario in test_scenarios:
        print(f"\n------------------------------------------------------------------")
        print(f"SCENARIO {scenario['id']}: {scenario['name']}")
        print(f"Input Criteria: Region={scenario['req'].region}, Niche={scenario['req'].niche}, Keywords={scenario['req'].keywords}")
        
        profiles, provider_used, is_demo, warning = await engine.execute_discovery(scenario['req'])
        
        print(f"Provider Used: {provider_used.upper()} | Is Demo: {is_demo} | Discovered Profiles: {len(profiles)}")
        if warning:
            print(f"Notice: {warning}")

        for idx, p in enumerate(profiles, start=1):
            print(f"\n  [Result #{idx}] @{p.username}")
            print(f"   * Display Name: {p.display_name or 'Not available'}")
            print(f"   * Profile URL: {p.profile_url}")
            print(f"   * Followers: {p.followers_formatted}")
            print(f"   * Detected Region: {p.region or 'Not available'}")
            print(f"   * Assigned Tags: {p.tags}")
            print(f"   * Match Score: {p.match_score}/100")
            print(f"   * Data Confidence: {p.data_confidence.value}")
            print(f"   * Match Reasons:")
            for r in p.match_reasons:
                print(f"      - {r.criterion}: {r.description} (+{r.score_contribution})")
            print(f"   * Snippet Excerpt: {p.bio[:90] if p.bio else 'Not available'}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_live_audit())
