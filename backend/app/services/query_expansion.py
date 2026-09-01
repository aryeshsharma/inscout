import re
from typing import List, Set, Dict
from app.models.search import SearchRequest

class QueryExpansionEngine:
    """
    INSCOUT Multi-Angle Semantic Query Expansion Engine.
    
    Dynamically generates 30-50+ independent, diverse query families to discover
    real public creators across diverse roles, bio phrases, content formats,
    regional clusters, and collaboration markers — eliminating username bias.
    """

    ROLE_SYNONYMS: Dict[str, List[str]] = {
        "Fashion": [
            "fashion creator", "fashion stylist", "fashion blogger", "fashion influencer", "fashion model",
            "wardrobe stylist", "street style creator", "lookbook creator", "ootd creator", "menswear stylist",
            "sustainable fashion", "ethnic wear creator", "style curator", "apparel stylist"
        ],
        "Travel": [
            "travel creator", "travel blogger", "travel vlogger", "travel filmmaker", "travel photographer",
            "backpacker", "wanderer", "solo traveler", "trekker", "road trip creator",
            "hidden gems explorer", "itinerary guide", "travel writer", "nomad", "adventure creator"
        ],
        "Beauty": [
            "beauty creator", "beauty blogger", "makeup artist", "mua", "skincare blogger",
            "bridal makeup artist", "hair stylist", "aesthetician", "cosmetics reviewer", "glam artist"
        ],
        "Technology": [
            "software developer", "tech creator", "coding educator", "fullstack engineer",
            "tech founder", "python developer", "webdev creator", "system architect",
            "devops engineer", "ai builder", "programmer", "tech reviewer"
        ],
        "Fitness": [
            "fitness coach", "personal trainer", "strength coach", "athlete", "bodybuilding",
            "calisthenics trainer", "wellness coach", "yoga instructor", "crossfit coach",
            "endurance runner", "nutrition coach"
        ],
        "Food": [
            "food creator", "food blogger", "chef", "baker", "recipe creator",
            "culinary artist", "home chef", "cafe explorer", "street food guide", "food reviewer"
        ],
        "Lifestyle": [
            "content creator", "lifestyle blogger", "lifestyle vlogger", "storyteller",
            "aesthetic creator", "daily vlog", "digital creator", "life curator"
        ],
        "Gaming": [
            "gaming creator", "streamer", "esports athlete", "twitch streamer", "gameplay creator"
        ],
        "Finance": [
            "finance creator", "investor", "stock trader", "fintech founder", "personal finance coach"
        ],
        "Music": [
            "musician", "singer", "music producer", "dj", "songwriter", "vocalist", "indie artist"
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
        "delhi": ["Delhi", "New Delhi", "Delhi NCR", "Gurgaon", "Gurugram", "Noida", "Faridabad", "Ghaziabad", "South Delhi", "Dwarka"],
        "mumbai": ["Mumbai", "Bombay", "Bandra", "Andheri", "Juhu", "Powai", "Navi Mumbai", "Thane", "South Mumbai"],
        "bangalore": ["Bangalore", "Bengaluru", "Indiranagar", "Koramangala", "HSR Layout", "Whitefield", "Jayanagar"],
        "hyderabad": ["Hyderabad", "Secunderabad", "Cyberabad", "Jubilee Hills", "Banjara Hills", "Gachibowli", "Hitec City"],
        "chennai": ["Chennai", "Madras", "Adyar", "Anna Nagar", "T Nagar", "Besant Nagar"],
        "kolkata": ["Kolkata", "Calcutta", "Salt Lake", "New Town", "Park Street"],
        "pune": ["Pune", "Kothrud", "Viman Nagar", "Baner", "Koregaon Park", "Aundh"],
        "ahmedabad": ["Ahmedabad", "Gandhinagar", "SG Highway", "Satellite"],
        "jaipur": ["Jaipur", "Pink City", "C Scheme", "Vaishali Nagar"],
        "chandigarh": ["Chandigarh", "Mohali", "Panchkula", "Tricity"],
        "lucknow": ["Lucknow", "Gomti Nagar", "Hazratganj"],
        "goa": ["Goa", "Panjim", "North Goa", "South Goa", "Anjuna"]
    }

    BIO_INTENT_SIGNALS: List[str] = [
        "DM for collabs",
        "PR / collaborations",
        "collabs",
        "collaborations",
        "bookings / inquiries",
        "UGC creator",
        "content creator",
        "inquiries",
        "work with me"
    ]

    CONTENT_FORMATS: Dict[str, List[str]] = {
        "Fashion": ["ootd", "lookbook", "styling reels", "street style", "outfit ideas"],
        "Travel": ["travel vlogs", "weekend getaways", "itinerary", "hidden gems", "road trips", "travel reels"],
        "Beauty": ["makeup tutorial", "swatches", "skincare routine", "glam look", "beauty tips"],
        "Technology": ["coding tips", "tech review", "developer roadmap", "software architecture", "tech reels"],
        "Food": ["cafe reviews", "street food guide", "easy recipes", "food tasting"],
        "Lifestyle": ["daily vlog", "aesthetic reels", "day in my life", "curated living"]
    }

    @classmethod
    def expand_queries(cls, request: SearchRequest, max_queries: int = 45) -> List[str]:
        queries: List[str] = []
        seen: Set[str] = set()

        raw_region = (request.region or "").strip()
        is_generic_region = not raw_region or "any region" in raw_region.lower() or raw_region.lower() == "india"
        primary_city = "" if is_generic_region else re.sub(r'[^\w\s]', '', raw_region)
        
        raw_niche = (request.niche or "").strip()
        clean_niche = "" if not raw_niche or raw_niche.lower() == "other" else re.sub(r'[^\w\s]', '', raw_niche)
        
        user_kws = [re.sub(r'[^\w\s]', '', k.strip()) for k in request.keywords if k.strip()]
        roles = cls.ROLE_SYNONYMS.get(clean_niche, cls.ROLE_SYNONYMS["Other"])
        formats = cls.CONTENT_FORMATS.get(clean_niche, ["content creator", "reels", "vlogs"])

        city_aliases = [primary_city] if primary_city else []
        city_lower = primary_city.lower()
        if city_lower in cls.REGIONAL_CLUSTERS:
            city_aliases = cls.REGIONAL_CLUSTERS[city_lower]

        def add_q(q_str: str):
            q_clean = " ".join(q_str.split()).strip()
            if q_clean and q_clean not in seen and len(queries) < max_queries:
                seen.add(q_clean)
                queries.append(q_clean)

        # Family 1: Bio Location Phrases (e.g. site:instagram.com "based in Mumbai" travel)
        for sig in ["based in", "living in", "from"]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com "{sig} {primary_city}" {clean_niche}')
                add_q(f'site:instagram.com "{sig} {primary_city}" {roles[0]}')
            elif primary_city:
                add_q(f'site:instagram.com "{sig} {primary_city}" creator')

        # Family 2: Location + Role Synonyms (e.g. site:instagram.com Mumbai "travel filmmaker")
        for role in roles[:8]:
            if primary_city:
                add_q(f'site:instagram.com {primary_city} "{role}"')
            elif clean_niche:
                add_q(f'site:instagram.com "{role}"')

        # Family 3: Location + Content Type Formats (e.g. site:instagram.com Mumbai "travel vlogs")
        for fmt in formats[:4]:
            if primary_city:
                add_q(f'site:instagram.com {primary_city} "{fmt}"')
            elif clean_niche:
                add_q(f'site:instagram.com "{fmt}"')

        # Family 4: Collaboration & PR Intent Dorks (e.g. site:instagram.com Mumbai travel "DM for collabs")
        for b_sig in cls.BIO_INTENT_SIGNALS[:4]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com {primary_city} {clean_niche} "{b_sig}"')
            elif primary_city:
                add_q(f'site:instagram.com {primary_city} "{b_sig}"')

        # Family 5: Regional Cluster Neighborhoods (e.g. Bandra, Andheri for Mumbai; Gurgaon for Delhi)
        if len(city_aliases) > 1 and clean_niche:
            for alias in city_aliases[1:6]:
                add_q(f'site:instagram.com {alias} {clean_niche} creator')
                add_q(f'site:instagram.com "{alias}" "{roles[0]}"')

        # Family 6: User-Supplied Bio Keywords Combined with City and Niche
        for ukw in user_kws[:4]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com {primary_city} {clean_niche} "{ukw}"')
            elif primary_city:
                add_q(f'site:instagram.com {primary_city} "{ukw}"')

        # Family 7: Inverted Query Patterns & Hashtags
        if primary_city and clean_niche:
            add_q(f'site:instagram.com "{clean_niche} creator" "{primary_city}"')
            add_q(f'site:instagram.com #{primary_city.lower().replace(" ", "")}{clean_niche.lower().replace(" ", "")}')

        return queries
