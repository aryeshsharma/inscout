import re
from typing import List
from app.models.search import SearchRequest

class QueryGenerator:
    """
    Generates targeted search queries and boolean search dorks
    for public web Instagram profile discovery without paid APIs.
    """
    
    @staticmethod
    def generate_dork_query(request: SearchRequest) -> str:
        parts = ["site:instagram.com"]
        
        region = request.region.strip() if request.region else ""
        if region and "any region" not in region.lower() and region.lower() != "india":
            clean_region = re.sub(r'[^\w\s]', '', region)
            parts.append(f'"{clean_region}"')
        elif region and region.lower() == "india":
            parts.append("India")
            
        niche = request.niche.strip() if request.niche else ""
        if niche and niche.lower() != "other":
            clean_niche = re.sub(r'[^\w\s]', '', niche)
            parts.append(f'"{clean_niche}"')
            
        clean_keywords = []
        for kw in request.keywords:
            kw_clean = re.sub(r'[^\w\s]', '', kw.strip())
            if kw_clean:
                clean_keywords.append(kw_clean)
                
        if clean_keywords:
            parts.append(" ".join(clean_keywords[:3]))
                
        return " ".join(parts)

    @staticmethod
    def generate_layered_queries(request: SearchRequest) -> List[str]:
        """
        Generates progressive, layered queries for public web search discovery.
        """
        queries = []
        
        region = request.region.strip() if request.region else ""
        has_specific_region = region and "any region" not in region.lower()
        clean_region = re.sub(r'[^\w\s]', '', region) if has_specific_region else ""
        
        niche = request.niche.strip() if request.niche else ""
        clean_niche = re.sub(r'[^\w\s]', '', niche) if niche and niche.lower() != "other" else ""
        
        clean_kws = [re.sub(r'[^\w\s]', '', k.strip()) for k in request.keywords if k.strip()]

        # Strategy 1: site:instagram.com with region & niche
        s1 = ["site:instagram.com"]
        if clean_region:
            s1.append(f'"{clean_region}"')
        if clean_niche:
            s1.append(clean_niche)
        if clean_kws:
            s1.append(clean_kws[0])
        queries.append(" ".join(s1))

        # Strategy 2: instagram.com/ with natural terms
        s2 = ["instagram.com/"]
        if clean_region:
            s2.append(clean_region)
        if clean_niche:
            s2.append(clean_niche)
        if len(clean_kws) > 1:
            s2.append(clean_kws[1])
        queries.append(" ".join(s2))

        # Strategy 3: instagram profile creator query
        s3 = ["instagram"]
        if clean_region:
            s3.append(clean_region)
        if clean_niche:
            s3.append(clean_niche)
        s3.append("creator")
        queries.append(" ".join(s3))

        return queries
