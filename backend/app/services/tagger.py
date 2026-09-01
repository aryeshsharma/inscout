import re
from typing import List, Set

class TaggingEngine:
    """
    Deterministic rule- and taxonomy-based tagging engine.
    Analyzes profile bios, display names, and public search context.
    """
    
    NICHE_TAXONOMY = {
        "Fashion": [
            "fashion", "style", "styling", "outfit", "ootd", "lookbook", "wardrobe",
            "couture", "apparel", "streetwear", "model", "modeling", "runway", "fashionista"
        ],
        "Beauty": [
            "beauty", "makeup", "skincare", "mua", "cosmetics", "hair", "glam",
            "dermatology", "aesthetic", "glow", "fragrance", "nails", "salon"
        ],
        "Lifestyle": [
            "lifestyle", "daily", "vlog", "vlogger", "creator", "aesthetic", "inspire",
            "mindfulness", "homedecor", "living", "storyteller", "curator"
        ],
        "Fitness": [
            "fitness", "gym", "workout", "trainer", "coach", "bodybuilding", "athlete",
            "yoga", "pilates", "crossfit", "calisthenics", "health", "wellness", "nutrition"
        ],
        "Food": [
            "food", "foodie", "chef", "baker", "recipe", "culinary", "restaurant",
            "cafe", "cooking", "gastronomy", "streetfood", "delicious", "dining", "eats"
        ],
        "Travel": [
            "travel", "wanderlust", "traveler", "explore", "backpacking", "destinations",
            "itinerary", "voyage", "adventure", "nomad", "travelgram", "trips"
        ],
        "Technology": [
            "tech", "technology", "developer", "coding", "software", "ai", "engineer",
            "gadgets", "web3", "startup", "python", "javascript", "cloud", "saas", "hardware"
        ],
        "Gaming": [
            "gaming", "gamer", "esports", "streamer", "twitch", "gameplay", "fps",
            "playstation", "xbox", "pcgamer", "youtube gaming"
        ],
        "Finance": [
            "finance", "money", "investing", "stocks", "crypto", "trading", "wealth",
            "fintech", "financial", "economics", "realestate", "investor"
        ],
        "Music": [
            "music", "musician", "singer", "dj", "producer", "composer", "guitar",
            "beats", "artist", "vocals", "band", "songwriter", "rap"
        ],
        "Photography": [
            "photography", "photographer", "photo", "lens", "canon", "sony", "nikon",
            "portrait", "cinematography", "videographer", "visuals", "photomodel"
        ],
        "Art": [
            "art", "artist", "design", "designer", "illustrator", "sketch", "digital art",
            "creative", "typography", "graphic designer", "painting", "craft"
        ],
        "Education": [
            "education", "educator", "teacher", "learning", "study", "student", "courses",
            "knowledge", "academy", "tutorial", "skills", "upskilling"
        ],
        "Business": [
            "business", "entrepreneur", "founder", "marketing", "ecommerce", "brand",
            "consulting", "agency", "leadership", "executive", "smallbusiness"
        ],
        "Comedy": [
            "comedy", "comedian", "standup", "funny", "humor", "skits", "memes",
            "parody", "roast", "entertainer", "jokes"
        ],
        "Sports": [
            "sports", "cricket", "football", "badminton", "athlete", "tournament",
            "championship", "running", "marathon", "tennis", "basketball"
        ],
        "Health": [
            "health", "doctor", "medical", "wellness", "nutritionist", "mentalhealth",
            "therapy", "holistic", "diet", "immunity", "healing"
        ]
    }
    
    ROLE_KEYWORDS = {
        "Model": ["model", "modelling", "runway", "editorial", "portfolio"],
        "Content Creator": ["creator", "content creator", "digital creator", "influencer", "blogger"],
        "Stylist": ["stylist", "fashion stylist", "wardrobe stylist", "celebrity stylist"],
        "Coach / Trainer": ["coach", "trainer", "fitness coach", "mentor", "consultant"],
        "Developer": ["developer", "software engineer", "coder", "programmer"],
        "Founder": ["founder", "co-founder", "ceo", "entrepreneur", "builder"],
        "Chef": ["chef", "cook", "culinary artist", "home chef", "pastry chef"],
        "Photographer": ["photographer", "videographer", "filmmaker", "cinematographer"],
        "Artist": ["artist", "illustrator", "painter", "sculptor"]
    }
    
    REGION_KEYWORDS = {
        "Delhi": ["delhi", "new delhi", "ncr", "gurugram", "gurgaon", "noida", "south delhi", "delhi ncr"],
        "Mumbai": ["mumbai", "bombay", "bandra", "andheri", "south mumbai", "navi mumbai", "thane"],
        "Bangalore": ["bangalore", "bengaluru", "indiranagar", "koramangala", "whitefield", "hsr layout"],
        "Hyderabad": ["hyderabad", "secunderabad", "cyberabad", "jubilee hills", "banjara hills", "gachibowli"],
        "Chennai": ["chennai", "madras", "adyar", "t nagar", "anna nagar"],
        "Kolkata": ["kolkata", "calcutta", "salt lake", "new town kolkata"],
        "Pune": ["pune", "punekar", "koregaon park", "kothrud", "viman nagar", "baner"],
        "Ahmedabad": ["ahmedabad", "gujarat", "gandhinagar"],
        "Jaipur": ["jaipur", "pink city", "rajasthan"],
        "Chandigarh": ["chandigarh", "mohali", "panchkula", "tricity"],
        "Gurgaon": ["gurgaon", "gurugram", "cyber city", "dlf"],
        "Noida": ["noida", "greater noida", "noida extension"],
        "Lucknow": ["lucknow", "gomti nagar", "hazratganj"],
        "Indore": ["indore", "madhya pradesh"],
        "Kochi": ["kochi", "cochin", "ernakulam", "kerala"],
        "Goa": ["goa", "panjim", "north goa", "south goa"]
    }
    
    COLLAB_SIGNALS = [
        "collab", "collabs", "collaboration", "collaborations", "dm for collab",
        "dm for collabs", "dm for collaborations", "pr", "inquiries", "management",
        "bookings", "brand ambassador", "press"
    ]

    @classmethod
    def extract_tags(cls, text: str, user_query_niche: str = "", user_keywords: List[str] = None) -> List[str]:
        if not text:
            text = ""
        text_lower = text.lower()
        tags: Set[str] = set()
        
        # 1. Match Niches
        for niche, keywords in cls.NICHE_TAXONOMY.items():
            for kw in keywords:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text_lower):
                    tags.add(niche)
                    break
                    
        # 2. Match Roles
        for role, keywords in cls.ROLE_KEYWORDS.items():
            for kw in keywords:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text_lower):
                    tags.add(role)
                    break
                    
        # 3. Match Collab Intent
        for signal in cls.COLLAB_SIGNALS:
            pattern = r'\b' + re.escape(signal) + r'\b'
            if re.search(pattern, text_lower):
                tags.add("Open for Collabs")
                break
                
        # 4. If user searched a niche and it appears in text, ensure it's included
        if user_query_niche and user_query_niche.lower() in text_lower:
            tags.add(user_query_niche.title())
            
        # 5. Check user provided keywords
        if user_keywords:
            for ukw in user_keywords:
                if ukw and re.search(r'\b' + re.escape(ukw.lower()) + r'\b', text_lower):
                    tags.add(ukw.title())

        # Sort tags
        return sorted(list(tags))

    @classmethod
    def detect_region(cls, text: str) -> str:
        if not text:
            return ""
        text_lower = text.lower()
        for region_name, variations in cls.REGION_KEYWORDS.items():
            for var in variations:
                if re.search(r'\b' + re.escape(var) + r'\b', text_lower):
                    return region_name
        return ""
