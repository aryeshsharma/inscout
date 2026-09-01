import re
from typing import List, Dict, Any
from app.models.search import SearchRequest
from app.services.tagger import TaggingEngine

class QueryExpansionEngine:
    """
    Expands a single user search request into a comprehensive suite of
    semantically diverse discovery queries across multiple search angles.
    """

    ROLE_SYNONYMS = {
        "Fashion": ["creator", "influencer", "blogger", "model", "stylist", "fashion designer", "content creator", "streetwear", "lookbook", "wardrobe stylist"],
        "Beauty": ["makeup artist", "mua", "beauty creator", "skincare blogger", "beauty influencer", "hair stylist", "aesthetician", "cosmetics"],
        "Lifestyle": ["creator", "influencer", "blogger", "vlogger", "content creator", "storyteller", "aesthetic creator"],
        "Fitness": ["trainer", "coach", "fitness coach", "personal trainer", "athlete", "bodybuilding", "calisthenics", "gym coach", "wellness coach"],
        "Food": ["foodie", "chef", "food blogger", "baker", "recipe creator", "culinary artist", "home chef", "food creator"],
        "Travel": ["traveler", "travel blogger", "nomad", "travel creator", "explorer", "backpacking", "travel vlog"],
        "Technology": ["developer", "software engineer", "tech creator", "coder", "programmer", "ai builder", "tech founder"],
        "Gaming": ["gamer", "streamer", "esports player", "gaming creator", "twitch streamer"],
        "Finance": ["investor", "finance creator", "trader", "fintech founder", "money mentor", "stock trader"],
        "Music": ["musician", "singer", "dj", "music producer", "artist", "composer", "songwriter"],
        "Photography": ["photographer", "cinematographer", "videographer", "portrait photographer", "visual artist"],
        "Art": ["artist", "illustrator", "designer", "digital artist", "painter", "graphic designer"],
        "Education": ["educator", "teacher", "mentor", "trainer", "academic", "coach"],
        "Business": ["founder", "entrepreneur", "ceo", "brand builder", "marketer", "business coach"],
        "Comedy": ["comedian", "standup comic", "humor creator", "entertainer", "meme creator"],
        "Sports": ["athlete", "player", "sports coach", "cricketer", "runner", "trainer"],
        "Health": ["nutritionist", "dietitian", "wellness coach", "doctor", "health creator"]
    }

    @classmethod
    def expand_queries(cls, request: SearchRequest, max_queries: int = 30) -> List[str]:
        queries: List[str] = []
        seen: set = set()

        region = (request.region or "").strip()
        is_generic_region = not region or "any region" in region.lower() or region.lower() == "india"
        clean_region = "" if is_generic_region else re.sub(r'[^\w\s]', '', region)
        
        niche = (request.niche or "").strip()
        clean_niche = "" if not niche or niche.lower() == "other" else re.sub(r'[^\w\s]', '', niche)
        
        user_kws = [re.sub(r'[^\w\s]', '', k.strip()) for k in request.keywords if k.strip()]
        roles = cls.ROLE_SYNONYMS.get(niche, ["creator", "influencer", "blogger", "model", "expert", "specialist"])

        def add_q(q_str: str):
            q_clean = " ".join(q_str.split()).strip()
            if q_clean and q_clean not in seen and len(queries) < max_queries:
                seen.add(q_clean)
                queries.append(q_clean)

        # 1. Site dorks with Role Synonyms
        for role in roles[:8]:
            if clean_region and clean_niche:
                add_q(f'site:instagram.com "{clean_region}" {clean_niche} {role}')
                add_q(f'site:instagram.com {clean_region} {role}')
            elif clean_region:
                add_q(f'site:instagram.com "{clean_region}" {role}')
            elif clean_niche:
                add_q(f'site:instagram.com {clean_niche} {role}')

        # 2. User Keyword combinations
        for ukw in user_kws:
            if clean_region and clean_niche:
                add_q(f'site:instagram.com "{clean_region}" {clean_niche} {ukw}')
                add_q(f'site:instagram.com {clean_region} {ukw}')
            elif clean_region:
                add_q(f'site:instagram.com "{clean_region}" {ukw}')
            elif clean_niche:
                add_q(f'site:instagram.com {clean_niche} {ukw}')

        # 3. Natural Instagram URL queries
        for role in roles[:5]:
            if clean_region and clean_niche:
                add_q(f'instagram.com/ {clean_region} {clean_niche} {role}')
            elif clean_region:
                add_q(f'instagram.com/ {clean_region} {role}')
            elif clean_niche:
                add_q(f'instagram.com/ {clean_niche} {role}')

        # 4. Hashtag Discovery Queries
        if clean_region and clean_niche:
            tag1 = f"#{clean_region.lower()}{clean_niche.lower()}"
            tag2 = f"#{clean_region.lower()}creator"
            tag3 = f"#{clean_region.lower()}blogger"
            add_q(f'site:instagram.com "{tag1}"')
            add_q(f'site:instagram.com "{tag2}"')
            add_q(f'site:instagram.com "{tag3}"')
        elif clean_niche:
            tag_niche = f"#{clean_niche.lower()}creator"
            add_q(f'site:instagram.com "{tag_niche}"')

        # 5. Inverted Niche-First Queries
        if clean_niche and clean_region:
            add_q(f'site:instagram.com {clean_niche} creator based in {clean_region}')
            add_q(f'site:instagram.com {clean_niche} model {clean_region}')
            add_q(f'site:instagram.com {clean_niche} influencer {clean_region}')

        return queries

if __name__ == "__main__":
    req = SearchRequest(
        region="Delhi",
        niche="Fashion",
        followers_min=10000,
        followers_max=100000,
        keywords=["model", "creator"]
    )
    expanded = QueryExpansionEngine.expand_queries(req, max_queries=30)
    print(f"Generated {len(expanded)} queries:")
    for i, q in enumerate(expanded, 1):
        print(f" {i:2d}. {q}")
