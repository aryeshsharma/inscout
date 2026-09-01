import re
from typing import List, Set, Dict
from app.models.search import SearchRequest

class QueryExpansionEngine:
    """
    INSCOUT Multi-Query Discovery Expansion Engine.
    
    Dynamically generates 30-50+ independent, diverse query families designed to
    discover genuine public creators through bio signals, collaboration markers,
    role specializations, and regional cluster dorks — completely bypassing username bias.
    """

    ROLE_SYNONYMS: Dict[str, List[str]] = {
        "Fashion": [
            "fashion creator", "fashion stylist", "fashion blogger", "fashion influencer", "fashion model",
            "wardrobe stylist", "streetwear creator", "lookbook", "ootd creator", "menswear stylist",
            "sustainable fashion", "ethnic wear stylist", "commercial model", "style curator"
        ],
        "Travel": [
            "travel creator", "travel blogger", "travel vlogger", "travel filmmaker", "travel photographer",
            "backpacker", "wanderer", "solo traveler", "trekker", "road trip creator",
            "itinerary guide", "travel writer", "nomad"
        ],
        "Beauty": [
            "makeup artist", "mua", "beauty creator", "skincare blogger", "bridal makeup artist",
            "hair stylist", "aesthetician", "cosmetics reviewer", "glam artist", "skincare expert"
        ],
        "Technology": [
            "software developer", "tech creator", "coding educator", "fullstack engineer",
            "tech founder", "python developer", "webdev creator", "system architect",
            "devops engineer", "ai builder", "programmer"
        ],
        "Fitness": [
            "fitness coach", "personal trainer", "strength coach", "athlete", "bodybuilding",
            "calisthenics trainer", "wellness coach", "yoga instructor", "crossfit coach",
            "endurance runner", "nutrition coach"
        ],
        "Food": [
            "food creator", "food blogger", "chef", "baker", "recipe creator",
            "culinary artist", "home chef", "cafe explorer", "street food guide"
        ],
        "Lifestyle": [
            "content creator", "lifestyle blogger", "vlogger", "storyteller",
            "aesthetic creator", "daily vlog", "digital creator", "curator"
        ],
        "Gaming": [
            "gaming creator", "streamer", "esports athlete", "twitch streamer", "gameplay creator"
        ],
        "Finance": [
            "finance creator", "investor", "stock trader", "fintech founder", "personal finance coach"
        ],
        "Music": [
            "musician", "singer", "music producer", "dj", "songwriter", "vocalist"
        ],
        "Photography": [
            "photographer", "cinematographer", "videographer", "portrait photographer", "visual artist"
        ],
        "Art": [
            "artist", "illustrator", "digital artist", "painter", "graphic designer", "craft creator"
        ],
        "Education": [
            "educator", "teacher", "mentor", "trainer", "course creator", "study creator"
        ],
        "Business": [
            "founder", "entrepreneur", "startup builder", "brand builder", "marketer", "agency owner"
        ],
        "Comedy": [
            "comedian", "standup comic", "humor creator", "meme creator", "sketch comedy"
        ],
        "Sports": [
            "athlete", "sports coach", "cricketer", "footballer", "badminton player", "runner"
        ],
        "Health": [
            "nutritionist", "dietitian", "wellness coach", "holistic health", "doctor"
        ],
        "Other": [
            "creator", "influencer", "blogger", "artist", "specialist", "expert"
        ]
    }

    REGIONAL_CLUSTERS: Dict[str, List[str]] = {
        "delhi": ["Delhi", "New Delhi", "Delhi NCR", "Gurgaon", "Gurugram", "Noida", "Faridabad", "Ghaziabad"],
        "mumbai": ["Mumbai", "Bombay", "Bandra", "Andheri", "Juhu", "Navi Mumbai", "Thane"],
        "bangalore": ["Bangalore", "Bengaluru", "Indiranagar", "Koramangala", "HSR Layout", "Whitefield"],
        "hyderabad": ["Hyderabad", "Secunderabad", "Cyberabad", "Jubilee Hills", "Gachibowli"],
        "chennai": ["Chennai", "Madras", "Adyar", "Anna Nagar"],
        "kolkata": ["Kolkata", "Calcutta", "Salt Lake"],
        "pune": ["Pune", "Kothrud", "Viman Nagar", "Baner"],
        "ahmedabad": ["Ahmedabad", "Gandhinagar"],
        "jaipur": ["Jaipur", "Pink City"],
        "chandigarh": ["Chandigarh", "Mohali", "Panchkula"],
        "lucknow": ["Lucknow"],
        "goa": ["Goa", "Panjim"]
    }

    BIO_SIGNALS: List[str] = [
        "DM for collabs",
        "PR / collabs",
        "collabs",
        "collaborations",
        "bookings / inquiries",
        "contact",
        "UGC creator",
        "content creator",
        "based in",
        "living in"
    ]

    @classmethod
    def expand_queries(cls, request: SearchRequest, max_queries: int = 40) -> List[str]:
        queries: List[str] = []
        seen: Set[str] = set()

        raw_region = (request.region or "").strip()
        is_generic_region = not raw_region or "any region" in raw_region.lower() or raw_region.lower() == "india"
        primary_city = "" if is_generic_region else re.sub(r'[^\w\s]', '', raw_region)
        
        raw_niche = (request.niche or "").strip()
        clean_niche = "" if not raw_niche or raw_niche.lower() == "other" else re.sub(r'[^\w\s]', '', raw_niche)
        
        user_kws = [re.sub(r'[^\w\s]', '', k.strip()) for k in request.keywords if k.strip()]
        roles = cls.ROLE_SYNONYMS.get(clean_niche, cls.ROLE_SYNONYMS["Other"])

        city_aliases = [primary_city] if primary_city else []
        city_lower = primary_city.lower()
        if city_lower in cls.REGIONAL_CLUSTERS:
            city_aliases = cls.REGIONAL_CLUSTERS[city_lower]

        def add_q(q_str: str):
            q_clean = " ".join(q_str.split()).strip()
            if q_clean and q_clean not in seen and len(queries) < max_queries:
                seen.add(q_clean)
                queries.append(q_clean)

        # Family 1: Explicit Bio Location Phrases ("based in Delhi", "living in Delhi NCR")
        for sig in ["based in", "living in", "from"]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com "{sig} {primary_city}" "{clean_niche}"')
                add_q(f'site:instagram.com "{sig} {primary_city}" {roles[0]}')
            elif primary_city:
                add_q(f'site:instagram.com "{sig} {primary_city}" creator')

        # Family 2: Role Synonyms & Specialized Content Creators
        for role in roles[:10]:
            if primary_city:
                add_q(f'site:instagram.com "{primary_city}" "{role}"')
            elif clean_niche:
                add_q(f'site:instagram.com "{role}"')

        # Family 3: Collaboration & PR Dorks
        for b_sig in cls.BIO_SIGNALS[:6]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com "{primary_city}" "{clean_niche}" "{b_sig}"')
            elif primary_city:
                add_q(f'site:instagram.com "{primary_city}" "{b_sig}"')

        # Family 4: Regional Cluster Synonyms (e.g. Gurgaon, Noida for Delhi)
        if len(city_aliases) > 1 and clean_niche:
            for alias in city_aliases[1:6]:
                add_q(f'site:instagram.com "{alias}" "{clean_niche} creator"')
                add_q(f'site:instagram.com "{alias}" "{roles[0]}"')

        # Family 5: User-Supplied Keywords Combined with Region and Niche
        for ukw in user_kws[:4]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com "{primary_city}" "{clean_niche}" "{ukw}"')
            elif primary_city:
                add_q(f'site:instagram.com "{primary_city}" "{ukw}"')

        # Family 6: Inverted Structure and City, India markers
        if primary_city and clean_niche:
            add_q(f'site:instagram.com "{primary_city}, India" "{clean_niche}"')
            add_q(f'site:instagram.com "#{primary_city.lower().replace(" ", "")}{clean_niche.lower().replace(" ", "")}"')

        return queries
