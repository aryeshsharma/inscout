import re
from typing import List, Set, Dict
from app.models.search import SearchRequest

class QueryExpansionEngine:
    """
    INSCOUT Semantic Query Expansion Engine (Anti-Username-Bias).
    
    Generates 25-35 diverse, high-yielding discovery queries designed to discover
    genuine public creators through bio signals, contact markers, role synonyms,
    and regional cluster expansions rather than keyword-heavy usernames.
    """

    ROLE_SYNONYMS: Dict[str, List[str]] = {
        "Fashion": [
            "fashion creator", "fashion influencer", "stylist", "fashion blogger", "model", "lookbook",
            "streetwear creator", "wardrobe stylist", "fashion designer", "ootd creator",
            "menswear stylist", "ethnic fashion", "sustainable fashion", "style curator"
        ],
        "Travel": [
            "travel creator", "travel blogger", "travel vlogger", "travel photographer",
            "travel filmmaker", "backpacker", "wanderer", "nomad", "travel stories",
            "road trips", "trekker", "itinerary guide", "solo traveller"
        ],
        "Beauty": [
            "makeup artist", "mua", "beauty creator", "skincare blogger", "bridal makeup",
            "hair stylist", "aesthetician", "cosmetics review", "glam artist", "skincare expert"
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
            "gaming creator", "streamer", "esports athlete", "twitch streamer",
            "gameplay creator", "pc gamer"
        ],
        "Finance": [
            "finance creator", "investor", "stock trader", "fintech founder",
            "wealth coach", "personal finance", "money mentor"
        ],
        "Music": [
            "musician", "singer", "music producer", "dj", "songwriter",
            "vocalist", "composer", "sound artist"
        ],
        "Photography": [
            "photographer", "cinematographer", "videographer", "portrait photographer",
            "visual artist", "fashion photographer", "street photographer"
        ],
        "Art": [
            "artist", "illustrator", "digital artist", "painter", "graphic designer",
            "sketch artist", "calligrapher", "craft creator"
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
        "based in"
    ]

    @classmethod
    def expand_queries(cls, request: SearchRequest, max_queries: int = 35) -> List[str]:
        queries: List[str] = []
        seen: Set[str] = set()

        raw_region = (request.region or "").strip()
        is_generic_region = not raw_region or "any region" in raw_region.lower() or raw_region.lower() == "india"
        primary_city = "" if is_generic_region else re.sub(r'[^\w\s]', '', raw_region)
        
        raw_niche = (request.niche or "").strip()
        clean_niche = "" if not raw_niche or raw_niche.lower() == "other" else re.sub(r'[^\w\s]', '', raw_niche)
        
        user_kws = [re.sub(r'[^\w\s]', '', k.strip()) for k in request.keywords if k.strip()]
        roles = cls.ROLE_SYNONYMS.get(clean_niche, cls.ROLE_SYNONYMS["Other"])

        # Resolve regional cluster aliases
        city_aliases = [primary_city] if primary_city else []
        city_lower = primary_city.lower()
        if city_lower in cls.REGIONAL_CLUSTERS:
            city_aliases = cls.REGIONAL_CLUSTERS[city_lower]

        def add_q(q_str: str):
            q_clean = " ".join(q_str.split()).strip()
            if q_clean and q_clean not in seen and len(queries) < max_queries:
                seen.add(q_clean)
                queries.append(q_clean)

        # 1. Family 1: Bio Signal & Collaboration Inquiries (Discovers real creators, not keyword usernames)
        for sig in cls.BIO_SIGNALS[:5]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com "{primary_city}" "{clean_niche}" "{sig}"')
                add_q(f'site:instagram.com "based in {primary_city}" {clean_niche}')
            elif primary_city:
                add_q(f'site:instagram.com "{primary_city}" "{sig}"')
            elif clean_niche:
                add_q(f'site:instagram.com "{clean_niche}" "{sig}"')

        # 2. Family 2: Role Synonyms & Specialized Content Creators
        for role in roles[:8]:
            if primary_city:
                add_q(f'site:instagram.com "{primary_city}" {role}')
            elif clean_niche:
                add_q(f'site:instagram.com {role}')

        # 3. Family 3: Regional Cluster Synonyms (e.g., Gurgaon, Noida for Delhi)
        if len(city_aliases) > 1 and clean_niche:
            for alias in city_aliases[1:5]:
                add_q(f'site:instagram.com "{alias}" {clean_niche} creator')
                add_q(f'site:instagram.com "{alias}" {roles[0]}')

        # 4. Family 4: User-Supplied Keywords combined with Region
        for ukw in user_kws[:4]:
            if primary_city and clean_niche:
                add_q(f'site:instagram.com "{primary_city}" {clean_niche} {ukw}')
            elif primary_city:
                add_q(f'site:instagram.com "{primary_city}" {ukw}')
            elif clean_niche:
                add_q(f'site:instagram.com {clean_niche} {ukw}')

        # 5. Family 5: Natural URL Paths & Inverted Location Markers
        for role in roles[:4]:
            if primary_city:
                add_q(f'instagram.com/ "{primary_city}" {role}')
            elif clean_niche:
                add_q(f'instagram.com/ {role}')

        # 6. Family 6: Hashtag Communities
        if primary_city and clean_niche:
            city_slug = primary_city.lower().replace(" ", "")
            niche_slug = clean_niche.lower().replace(" ", "")
            add_q(f'site:instagram.com "#{city_slug}{niche_slug}"')
            add_q(f'site:instagram.com "#{city_slug}creators"')
        elif clean_niche:
            add_q(f'site:instagram.com "#{clean_niche.lower()}creator"')

        return queries
