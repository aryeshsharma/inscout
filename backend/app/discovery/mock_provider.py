import re
from typing import List, Dict, Any, Optional
from app.discovery.base import BaseDiscoveryProvider
from app.models.profile import DiscoveredProfile, ConfidenceLevel, ConfidenceDetail
from app.models.search import SearchRequest
from app.services.tagger import TaggingEngine
from app.services.scorer import ScoringEngine
from app.services.normalizer import ProfileNormalizer

DEMO_PROFILES_DATA: List[Dict[str, Any]] = [
    # Fashion & Lifestyle - Delhi
    {
        "username": "tanya.sharma.style",
        "display_name": "Tanya Sharma | Delhi Stylist",
        "bio": "Delhi NCR | Fashion & Lifestyle Creator | Model | Editorial styling | DM for collaborations & PR 📩",
        "followers": 42300,
        "region": "Delhi",
        "category": "Fashion & Lifestyle",
        "profile_image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        "following": 420,
        "posts": 612,
        "engagement_rate": 3.8
    },
    {
        "username": "rohit.verma.couture",
        "display_name": "Rohit Verma",
        "bio": "New Delhi | Runway Model & Menswear Stylist | Streetwear aesthetics | Inquiries: rohit@vermastyle.in",
        "followers": 78900,
        "region": "Delhi",
        "category": "Fashion",
        "profile_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        "following": 310,
        "posts": 489,
        "engagement_rate": 4.1
    },
    {
        "username": "ananya_delhistyles",
        "display_name": "Ananya Kapoor",
        "bio": "South Delhi 📍 | Wardrobe curator & creative director | Sustainable fashion & lookbooks | Collabs: ananya@agency.com",
        "followers": 18400,
        "region": "Delhi",
        "category": "Fashion",
        "profile_image": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80",
        "following": 512,
        "posts": 284,
        "engagement_rate": 5.2
    },
    {
        "username": "delhi_streetwear_hub",
        "display_name": "Kabir Mehta",
        "bio": "Gurgaon / Delhi | Streetwear Culture & Sneakerhead | OOTD & styling guides | Press & brand deals 👇",
        "followers": 115000,
        "region": "Delhi",
        "category": "Fashion",
        "profile_image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
        "following": 680,
        "posts": 830,
        "engagement_rate": 3.2
    },
    
    # Fashion & Beauty - Mumbai
    {
        "username": "priya.mumbai.glam",
        "display_name": "Priya Sen",
        "bio": "Bandra, Mumbai | Fashion & Beauty Creator | Celebrity MUA & Model | For bookings: contact@priyaglams.com",
        "followers": 89400,
        "region": "Mumbai",
        "category": "Beauty",
        "profile_image": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
        "following": 415,
        "posts": 510,
        "engagement_rate": 4.5
    },
    {
        "username": "aarav_mumbai_looks",
        "display_name": "Aarav Deshmukh",
        "bio": "Mumbai | Fashion Creator & Actor | Luxury styling, editorial shoots | Management: scout@talentmumbai.in",
        "followers": 142000,
        "region": "Mumbai",
        "category": "Fashion",
        "profile_image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80",
        "following": 520,
        "posts": 740,
        "engagement_rate": 3.9
    },
    {
        "username": "sanya.skinandstyle",
        "display_name": "Sanya Merchant",
        "bio": "Andheri West, Mumbai | Clean Beauty & Minimal Wardrobe | Skincare routines | DM for PR",
        "followers": 29800,
        "region": "Mumbai",
        "category": "Beauty",
        "profile_image": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=150&auto=format&fit=crop&q=80",
        "following": 390,
        "posts": 320,
        "engagement_rate": 4.8
    },

    # Tech & Software - Bangalore
    {
        "username": "karthik.codes",
        "display_name": "Karthik Raja | Tech Creator",
        "bio": "Bangalore / Bengaluru | Software Engineer & AI Builder | Coding tutorials, Python, Web3 & tech reviews 💻",
        "followers": 64200,
        "region": "Bangalore",
        "category": "Technology",
        "profile_image": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80",
        "following": 240,
        "posts": 410,
        "engagement_rate": 6.1
    },
    {
        "username": "meera_techdev",
        "display_name": "Meera Krishnan",
        "bio": "Koramangala, Bangalore | Tech Founder & Dev Advocate | Building open-source tools | Speaker & mentor",
        "followers": 38100,
        "region": "Bangalore",
        "category": "Technology",
        "profile_image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
        "following": 320,
        "posts": 195,
        "engagement_rate": 5.4
    },
    {
        "username": "bangalore_gadgetlab",
        "display_name": "Vikram Sethi",
        "bio": "Indiranagar, Bangalore | Consumer Tech & Gadget Reviews | Unboxing smartphones, setups & SaaS",
        "followers": 182000,
        "region": "Bangalore",
        "category": "Technology",
        "profile_image": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80",
        "following": 410,
        "posts": 920,
        "engagement_rate": 4.0
    },

    # Fitness & Health - Hyderabad & Pune
    {
        "username": "rahul.fitcore",
        "display_name": "Rahul Reddy | Fitness Coach",
        "bio": "Hyderabad | Certified Strength & Conditioning Coach | Calisthenics & nutrition plans | DM for training",
        "followers": 53400,
        "region": "Hyderabad",
        "category": "Fitness",
        "profile_image": "https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=150&auto=format&fit=crop&q=80",
        "following": 280,
        "posts": 560,
        "engagement_rate": 4.9
    },
    {
        "username": "sneha.yogaflow",
        "display_name": "Sneha Kulkarni",
        "bio": "Pune | Ashtanga Yoga Teacher & Wellness Creator | Daily mindfulness & mobility drills | Workshops 👇",
        "followers": 24800,
        "region": "Pune",
        "category": "Fitness",
        "profile_image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80",
        "following": 310,
        "posts": 410,
        "engagement_rate": 5.7
    },
    {
        "username": "arjun_ironlife",
        "display_name": "Arjun Rao",
        "bio": "Hyderabad / Secunderabad | Bodybuilding & High Performance Athlete | Gym routines & diet tips | Collabs: arjun@fit.in",
        "followers": 96200,
        "region": "Hyderabad",
        "category": "Fitness",
        "profile_image": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=150&auto=format&fit=crop&q=80",
        "following": 190,
        "posts": 620,
        "engagement_rate": 3.7
    },

    # Food & Culinary - Kolkata & Delhi
    {
        "username": "kolkata_foodvoyage",
        "display_name": "Debanjan Roy",
        "bio": "Kolkata | Foodie & Heritage Cuisine Explorer | Street food trails, hidden cafes & recipes | PR welcome",
        "followers": 67800,
        "region": "Kolkata",
        "category": "Food",
        "profile_image": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80",
        "following": 450,
        "posts": 780,
        "engagement_rate": 6.2
    },
    {
        "username": "delhi_bakes_by_simran",
        "display_name": "Chef Simran Kaur",
        "bio": "New Delhi | Pastry Chef & Baker | Artisanal desserts, baking masterclasses | Order & inquiries in bio",
        "followers": 34100,
        "region": "Delhi",
        "category": "Food",
        "profile_image": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&auto=format&fit=crop&q=80",
        "following": 380,
        "posts": 490,
        "engagement_rate": 5.0
    },

    # Travel & Adventure - Goa & Jaipur
    {
        "username": "roaming.natasha",
        "display_name": "Natasha D'Souza",
        "bio": "Goa 🌴 | Travel Storyteller & Nomad | Coastal gems, sustainable stays & slow travel | Brand collaborations ✉️",
        "followers": 82600,
        "region": "Goa",
        "category": "Travel",
        "profile_image": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=150&auto=format&fit=crop&q=80",
        "following": 610,
        "posts": 540,
        "engagement_rate": 4.6
    },
    {
        "username": "jaipur_heritage_walks",
        "display_name": "Manish Rathore",
        "bio": "Jaipur (Pink City) | Architectural Photographer & Culture Explorer | Forts, palaces & royal stories",
        "followers": 41200,
        "region": "Jaipur",
        "category": "Travel",
        "profile_image": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150&auto=format&fit=crop&q=80",
        "following": 340,
        "posts": 410,
        "engagement_rate": 5.8
    },

    # Finance & Business - Mumbai & Bangalore
    {
        "username": "fintech_with_neil",
        "display_name": "Neil Parekh",
        "bio": "Mumbai | Finance Educator & Investor | Simplifying stock market, mutual funds & wealth creation 📈",
        "followers": 175000,
        "region": "Mumbai",
        "category": "Finance",
        "profile_image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80",
        "following": 150,
        "posts": 620,
        "engagement_rate": 4.3
    },

    # Gaming & Esports - Delhi & Pune
    {
        "username": "shadow_sniper_in",
        "display_name": "Karan Malhotra",
        "bio": "Delhi NCR | Esports Athlete & Streamer | FPS gaming, highlights & setup tours 🎮 | Inquiries: karan@esports.in",
        "followers": 128000,
        "region": "Delhi",
        "category": "Gaming",
        "profile_image": "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=150&auto=format&fit=crop&q=80",
        "following": 340,
        "posts": 710,
        "engagement_rate": 5.5
    },

    # Music & Creative - Chennai & Delhi
    {
        "username": "aditya.beats.music",
        "display_name": "Aditya Varma",
        "bio": "Chennai | Music Producer & Indie Singer | Acoustic covers, production breakdowns | DM for bookings",
        "followers": 31500,
        "region": "Chennai",
        "category": "Music",
        "profile_image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80",
        "following": 420,
        "posts": 360,
        "engagement_rate": 6.8
    },
    {
        "username": "ria_acoustic",
        "display_name": "Ria Sen",
        "bio": "Delhi | Singer-Songwriter & Vocal Coach | Live gigs, indie pop | Bookings: ria@singers.in",
        "followers": 15200,
        "region": "Delhi",
        "category": "Music",
        "profile_image": "https://images.unsplash.com/photo-1534751516642-a171ed2e3f86?w=150&auto=format&fit=crop&q=80",
        "following": 290,
        "posts": 190,
        "engagement_rate": 7.1
    },

    # Profile with missing follower metrics (Testing edge cases)
    {
        "username": "delhi_rising_couture",
        "display_name": "Studio Couture Delhi",
        "bio": "Delhi | Bespoke atelier & bridal styling | Handcrafted Indian wear | Contact for private appointments",
        "followers": None, # Demonstrating 'Not available' handling
        "region": "Delhi",
        "category": "Fashion",
        "profile_image": None,
        "following": None,
        "posts": 120,
        "engagement_rate": None
    }
]

class MockDiscoveryProvider(BaseDiscoveryProvider):
    
    @property
    def provider_name(self) -> str:
        return "mock"
        
    @property
    def is_demo(self) -> bool:
        return True

    async def discover_profiles(self, request: SearchRequest) -> List[DiscoveredProfile]:
        results: List[DiscoveredProfile] = []
        
        for item in DEMO_PROFILES_DATA:
            bio_text = item.get("bio", "")
            display_name = item.get("display_name", "")
            raw_region = item.get("region") or TaggingEngine.detect_region(bio_text)
            
            # Extract tags using the TaggingEngine
            tags = TaggingEngine.extract_tags(
                text=f"{bio_text} {display_name}",
                user_query_niche=request.niche or "",
                user_keywords=request.keywords
            )
            
            followers = item.get("followers")
            
            # Compute match score & itemized reasons
            score, reasons, matched_kws = ScoringEngine.calculate_match_score(
                bio=bio_text,
                display_name=display_name,
                tags=tags,
                region=raw_region,
                followers=followers,
                request=request
            )
            
            # Evaluate confidence
            has_bio = bool(bio_text)
            has_followers = followers is not None
            has_region = bool(raw_region)
            conf_level, conf_details = ProfileNormalizer.evaluate_confidence(
                has_bio=has_bio,
                has_followers=has_followers,
                has_region_signal=has_region,
                is_direct_profile=True
            )
            
            # Add demo note to confidence details
            conf_details.append(ConfidenceDetail(
                field="simulation",
                level=ConfidenceLevel.HIGH,
                source="Demo Dataset",
                description="Simulated profile created for controlled MVP testing and demonstration"
            ))
            
            profile = DiscoveredProfile(
                username=item["username"],
                profile_url=f"https://www.instagram.com/{item['username']}/",
                display_name=display_name,
                bio=bio_text,
                followers=followers,
                followers_formatted=ProfileNormalizer.format_followers(followers),
                region=raw_region if raw_region else None,
                tags=tags,
                matched_keywords=matched_kws,
                match_score=score,
                match_reasons=reasons,
                data_confidence=conf_level,
                confidence_details=conf_details,
                is_demo=True,
                profile_image=item.get("profile_image"),
                following=item.get("following"),
                posts=item.get("posts"),
                engagement_rate=item.get("engagement_rate"),
                category=item.get("category")
            )
            
            results.append(profile)
            
        # Sort candidate results by Match Score in descending order
        results.sort(key=lambda p: p.match_score, reverse=True)
        
        # Apply max_results limit
        return results[:request.max_results]
