import re
from typing import List, Set, Tuple, Dict, Optional

class TaggingEngine:
    """
    Deterministic rule- and taxonomy-based tagging and qualification engine.
    Analyzes profile bios and text snippets WITHOUT username-bias.
    """
    
    NICHE_TAXONOMY: Dict[str, List[str]] = {
        "Fashion": [
            "fashion", "style", "styling", "outfit", "ootd", "lookbook", "wardrobe",
            "couture", "apparel", "streetwear", "model", "modeling", "runway", "fashionista",
            "menswear", "womenswear", "ethnic wear", "thrift", "sustainable fashion"
        ],
        "Beauty": [
            "beauty", "makeup", "skincare", "mua", "cosmetics", "hair", "glam",
            "dermatology", "aesthetic", "glow", "fragrance", "nails", "salon", "makeover"
        ],
        "Lifestyle": [
            "lifestyle", "daily", "vlog", "vlogger", "creator", "aesthetic", "inspire",
            "mindfulness", "homedecor", "living", "storyteller", "curator", "content creator"
        ],
        "Fitness": [
            "fitness", "gym", "workout", "trainer", "coach", "bodybuilding", "athlete",
            "yoga", "pilates", "crossfit", "calisthenics", "health", "wellness", "nutrition", "strength"
        ],
        "Food": [
            "food", "foodie", "chef", "baker", "recipe", "culinary", "restaurant",
            "cafe", "cooking", "gastronomy", "streetfood", "delicious", "dining", "eats"
        ],
        "Travel": [
            "travel", "wanderlust", "traveler", "traveller", "explore", "backpacking", "destinations",
            "itinerary", "voyage", "adventure", "nomad", "travelgram", "trips", "road trip", "trek"
        ],
        "Technology": [
            "tech", "technology", "developer", "coding", "software", "ai", "engineer",
            "gadgets", "web3", "startup", "python", "javascript", "cloud", "saas", "hardware", "programmer"
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
    
    ROLE_KEYWORDS: Dict[str, List[str]] = {
        "Model": ["model", "modelling", "runway", "editorial", "portfolio"],
        "Content Creator": ["creator", "content creator", "digital creator", "influencer", "blogger", "vlogger"],
        "Stylist": ["stylist", "fashion stylist", "wardrobe stylist", "celebrity stylist"],
        "Coach / Trainer": ["coach", "trainer", "fitness coach", "mentor", "consultant"],
        "Developer": ["developer", "software engineer", "coder", "programmer"],
        "Founder": ["founder", "co-founder", "ceo", "entrepreneur", "builder"],
        "Chef": ["chef", "cook", "culinary artist", "home chef", "pastry chef"],
        "Photographer": ["photographer", "videographer", "filmmaker", "cinematographer"],
        "Artist": ["artist", "illustrator", "painter", "sculptor"]
    }
    
    # Regional clusters mapped to canonical city names
    REGION_CLUSTERS: Dict[str, List[str]] = {
        "Delhi": ["delhi", "new delhi", "delhi ncr", "ncr", "gurugram", "gurgaon", "noida", "faridabad", "ghaziabad", "south delhi", "delhiite"],
        "Mumbai": ["mumbai", "bombay", "bandra", "andheri", "south mumbai", "navi mumbai", "thane", "juhu", "mumbaikar"],
        "Bangalore": ["bangalore", "bengaluru", "indiranagar", "koramangala", "whitefield", "hsr layout", "electronic city"],
        "Hyderabad": ["hyderabad", "secunderabad", "cyberabad", "jubilee hills", "banjara hills", "gachibowli", "hyderabadi"],
        "Chennai": ["chennai", "madras", "adyar", "t nagar", "anna nagar"],
        "Kolkata": ["kolkata", "calcutta", "salt lake", "new town kolkata"],
        "Pune": ["pune", "punekar", "koregaon park", "kothrud", "viman nagar", "baner"],
        "Ahmedabad": ["ahmedabad", "gujarat", "gandhinagar"],
        "Jaipur": ["jaipur", "pink city", "rajasthan"],
        "Chandigarh": ["chandigarh", "mohali", "panchkula", "tricity"],
        "Lucknow": ["lucknow", "gomti nagar", "hazratganj"],
        "Goa": ["goa", "panjim", "north goa", "south goa"]
    }
    
    COLLAB_SIGNALS = [
        "collab", "collabs", "collaboration", "collaborations", "dm for collab",
        "dm for collabs", "dm for collaborations", "pr", "inquiries", "management",
        "bookings", "brand ambassador", "press", "ugc"
    ]

    @classmethod
    def extract_tags(cls, bio_text: str = "", user_query_niche: str = "", user_keywords: List[str] = None, text: str = "") -> List[str]:
        """
        Extracts semantic tags exclusively from bio text and content snippets.
        """
        eval_text = bio_text or text or ""
        text_lower = eval_text.lower()
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
                
        # 4. If user searched a niche and it appears in bio text, ensure it's included
        if user_query_niche and user_query_niche.lower() in text_lower:
            tags.add(user_query_niche.title())
            
        # 5. Check user provided keywords in bio
        if user_keywords:
            for ukw in user_keywords:
                if ukw and re.search(r'\b' + re.escape(ukw.lower()) + r'\b', text_lower):
                    tags.add(ukw.title())

        return sorted(list(tags))

    @classmethod
    def detect_region_with_confidence(cls, bio_text: str, context_snippet: str = "") -> Tuple[Optional[str], str, str]:
        """
        Detects region STRICTLY from bio text and public content snippets.
        CRITICAL: Username and Title are explicitly excluded to prevent handle bias.
        """
        eval_text = f"{bio_text or ''} {context_snippet or ''}".lower()
        if not eval_text.strip():
            return None, "LOW", "No bio or context location available"
            
        # 1. High Confidence: Explicit location phrases
        for canonical_city, variations in cls.REGION_CLUSTERS.items():
            for var in variations:
                high_patterns = [
                    (r'\bbased in ' + re.escape(var) + r'\b', f"Explicit phrase 'based in {var.title()}' in bio"),
                    (r'\bliving in ' + re.escape(var) + r'\b', f"Explicit phrase 'living in {var.title()}' in bio"),
                    (r'\bfrom ' + re.escape(var) + r'\b', f"Explicit phrase 'from {var.title()}' in bio"),
                    (r'\blocated in ' + re.escape(var) + r'\b', f"Explicit phrase 'located in {var.title()}' in bio"),
                    (r'\b' + re.escape(var) + r'\s*,\s*india\b', f"Explicit 'location: {var.title()}, India' in bio"),
                    (r'\b' + re.escape(var) + r'\s*ncr\b', f"Explicit 'Delhi NCR / {var.title()} NCR' in bio"),
                    (r'\bnew ' + re.escape(var) + r'\b', f"Explicit 'New {var.title()}' in bio")
                ]
                for p, reason in high_patterns:
                    if re.search(p, eval_text):
                        return canonical_city, "HIGH", reason

        # 2. Medium Confidence: Word boundary match in bio text
        for canonical_city, variations in cls.REGION_CLUSTERS.items():
            for var in variations:
                if re.search(r'\b' + re.escape(var) + r'\b', eval_text):
                    return canonical_city, "MEDIUM", f"City/cluster mention '{var.title()}' detected in bio text"

        return None, "LOW", "No valid geographic evidence found in bio"

    @classmethod
    def detect_region(cls, bio_text: str) -> Optional[str]:
        reg, _, _ = cls.detect_region_with_confidence(bio_text)
        return reg
