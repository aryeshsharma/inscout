import re
from typing import List, Set
from app.models.search import SearchRequest

class QueryExpansionEngine:
    """
    Expands a user search request into a semantically diverse suite of targeted
    discovery queries without over-quoted dorks that search engines reject.
    """

    ROLE_SYNONYMS = {
        "Fashion": [
            "creator", "influencer", "blogger", "model", "stylist", "fashion designer",
            "content creator", "lookbook", "streetwear", "wardrobe stylist", "runway model",
            "fashionista", "style creator"
        ],
        "Beauty": [
            "makeup artist", "mua", "beauty creator", "skincare blogger", "beauty influencer",
            "hair stylist", "aesthetician", "cosmetics", "glam artist", "skincare expert",
            "makeup studio", "salon"
        ],
        "Lifestyle": [
            "creator", "influencer", "blogger", "vlogger", "content creator", "storyteller",
            "daily vlog", "curator", "aesthetic creator", "digital creator"
        ],
        "Fitness": [
            "trainer", "coach", "fitness coach", "personal trainer", "athlete", "bodybuilding",
            "calisthenics", "gym coach", "wellness coach", "yoga teacher", "fitness trainer",
            "gym trainer"
        ],
        "Food": [
            "foodie", "chef", "food blogger", "baker", "recipe creator", "culinary artist",
            "home chef", "food creator", "cafe explorer", "restaurant reviewer"
        ],
        "Travel": [
            "traveler", "travel blogger", "nomad", "travel creator", "explorer", "backpacking",
            "travel vlog", "wanderer", "destination guide"
        ],
        "Technology": [
            "developer", "software engineer", "tech creator", "coder", "programmer", "ai builder",
            "tech founder", "devops engineer", "web developer", "python developer", "software developer"
        ],
        "Gaming": [
            "gamer", "streamer", "esports player", "gaming creator", "twitch streamer",
            "gameplay creator", "pc gamer"
        ],
        "Finance": [
            "investor", "finance creator", "trader", "fintech founder", "money mentor",
            "stock trader", "wealth creator", "personal finance"
        ],
        "Music": [
            "musician", "singer", "dj", "music producer", "artist", "composer", "songwriter",
            "vocalist", "sound engineer"
        ],
        "Photography": [
            "photographer", "cinematographer", "videographer", "portrait photographer",
            "visual artist", "fashion photographer", "camera artist"
        ],
        "Art": [
            "artist", "illustrator", "designer", "digital artist", "painter", "graphic designer",
            "sketch artist", "craft creator"
        ],
        "Education": [
            "educator", "teacher", "mentor", "trainer", "academic", "coach", "study creator",
            "course creator"
        ],
        "Business": [
            "founder", "entrepreneur", "ceo", "brand builder", "marketer", "business coach",
            "agency owner", "startup builder"
        ],
        "Comedy": [
            "comedian", "standup comic", "humor creator", "entertainer", "meme creator",
            "comedy sketches", "parody artist"
        ],
        "Sports": [
            "athlete", "player", "sports coach", "cricketer", "runner", "trainer", "sportsman",
            "badminton player"
        ],
        "Health": [
            "nutritionist", "dietitian", "wellness coach", "doctor", "health creator",
            "holistic health", "diet coach"
        ],
        "Other": [
            "creator", "influencer", "blogger", "specialist", "expert", "artist", "consultant"
        ]
    }

    CITY_ALIASES = {
        "delhi": ["Delhi", "Delhi NCR", "New Delhi"],
        "mumbai": ["Mumbai", "Bombay"],
        "bangalore": ["Bangalore", "Bengaluru"],
        "hyderabad": ["Hyderabad"],
        "chennai": ["Chennai", "Madras"],
        "kolkata": ["Kolkata", "Calcutta"],
        "pune": ["Pune"],
        "ahmedabad": ["Ahmedabad"],
        "jaipur": ["Jaipur"],
        "chandigarh": ["Chandigarh"],
        "gurgaon": ["Gurgaon", "Gurugram"],
        "noida": ["Noida"],
        "lucknow": ["Lucknow"],
        "indore": ["Indore"],
        "kochi": ["Kochi", "Cochin"],
        "goa": ["Goa"]
    }

    @classmethod
    def expand_queries(cls, request: SearchRequest, max_queries: int = 30) -> List[str]:
        queries: List[str] = []
        seen: Set[str] = set()

        raw_region = (request.region or "").strip()
        is_generic_region = not raw_region or "any region" in raw_region.lower() or raw_region.lower() == "india"
        clean_region = "" if is_generic_region else re.sub(r'[^\w\s]', '', raw_region)
        
        raw_niche = (request.niche or "").strip()
        clean_niche = "" if not raw_niche or raw_niche.lower() == "other" else re.sub(r'[^\w\s]', '', raw_niche)
        
        user_kws = [re.sub(r'[^\w\s]', '', k.strip()) for k in request.keywords if k.strip()]
        roles = cls.ROLE_SYNONYMS.get(clean_niche, cls.ROLE_SYNONYMS["Other"])

        def add_q(q_str: str):
            q_clean = " ".join(q_str.split()).strip()
            if q_clean and q_clean not in seen and len(queries) < max_queries:
                seen.add(q_clean)
                queries.append(q_clean)

        # 1. Natural Site Dorks with Role Synonyms
        for role in roles[:8]:
            if clean_region and clean_niche:
                add_q(f'site:instagram.com {clean_region} {clean_niche} {role}')
                add_q(f'site:instagram.com {clean_region} {role}')
            elif clean_region:
                add_q(f'site:instagram.com {clean_region} {role}')
            elif clean_niche:
                add_q(f'site:instagram.com {clean_niche} {role}')

        # 2. User Keyword combinations
        for ukw in user_kws[:4]:
            if clean_region and clean_niche:
                add_q(f'site:instagram.com {clean_region} {clean_niche} {ukw}')
                add_q(f'site:instagram.com {clean_region} {ukw}')
            elif clean_region:
                add_q(f'site:instagram.com {clean_region} {ukw}')
            elif clean_niche:
                add_q(f'site:instagram.com {clean_niche} {ukw}')

        # 3. Hashtag-Based Discovery Dorks
        if clean_region and clean_niche:
            tag_city_niche = f"#{clean_region.lower().replace(' ', '')}{clean_niche.lower()}"
            tag_city_creator = f"#{clean_region.lower().replace(' ', '')}creator"
            add_q(f'site:instagram.com {tag_city_niche}')
            add_q(f'site:instagram.com {tag_city_creator}')
        elif clean_niche:
            tag_niche = f"#{clean_niche.lower()}creator"
            add_q(f'site:instagram.com {tag_niche}')

        # 4. Natural URL Patterns
        for role in roles[:5]:
            if clean_region and clean_niche:
                add_q(f'instagram.com/ {clean_region} {clean_niche} {role}')
            elif clean_region:
                add_q(f'instagram.com/ {clean_region} {role}')
            elif clean_niche:
                add_q(f'instagram.com/ {clean_niche} {role}')

        # 5. Inverted Niche-First Natural Queries
        if clean_niche and clean_region:
            add_q(f'site:instagram.com {clean_niche} creator based in {clean_region}')
            add_q(f'site:instagram.com {clean_niche} influencer {clean_region}')

        # 6. City Alias variations
        city_lower = clean_region.lower()
        if city_lower in cls.CITY_ALIASES and clean_niche:
            for alias in cls.CITY_ALIASES[city_lower]:
                if alias.lower() != clean_region.lower():
                    add_q(f'site:instagram.com {alias} {clean_niche} creator')
                    add_q(f'site:instagram.com {alias} {clean_niche} influencer')

        return queries
