import re
from typing import Optional, Tuple, List
from urllib.parse import urlparse
from app.models.profile import ConfidenceLevel, ConfidenceDetail

# Reserved path segments on Instagram that are not user profiles
RESERVED_USERNAMES = {
    "explore", "p", "reel", "reels", "tv", "stories", "tags", "locations",
    "direct", "accounts", "about", "legal", "developer", "terms", "privacy",
    "directory", "press", "help", "support", "cookie", "login", "signup"
}

class ProfileNormalizer:
    
    @staticmethod
    def extract_username_from_url(url: str) -> Optional[str]:
        if not url:
            return None
        try:
            parsed = urlparse(url)
            if "instagram.com" not in parsed.netloc.lower():
                return None
            path = parsed.path.strip("/").split("/")
            if not path or not path[0]:
                return None
            username = path[0].lower().replace("@", "").strip()
            if username in RESERVED_USERNAMES or len(username) > 30:
                return None
            # Instagram usernames only contain letters, numbers, periods, and underscores
            if not re.match(r'^[a-zA-Z0-9._]+$', username):
                return None
            return username
        except Exception:
            return None

    @staticmethod
    def extract_display_name(title: str, username: Optional[str] = None) -> Optional[str]:
        if not title:
            return None
        # Common title formats:
        # "Jane Doe (@janedoe) • Instagram photos and videos"
        # "Jane Doe (@janedoe) on Instagram: 'Bio text...'"
        # "Jane Doe • Instagram"
        clean_title = title.split("•")[0].split("on Instagram")[0].split("- Instagram")[0].split("| Instagram")[0]
        # Remove (@username)
        clean_title = re.sub(r'\(@[a-zA-Z0-9._]+\)', '', clean_title)
        clean_title = clean_title.strip()
        if clean_title and (username is None or clean_title.lower() != username.lower()):
            return clean_title
        return None

    @staticmethod
    def parse_follower_count(text: str) -> Optional[int]:
        if not text:
            return None
        # Match patterns like:
        # "42.5K Followers", "1.2M Followers", "50,000 Followers", "Followers: 12.3k", "45k followers"
        patterns = [
            r'([\d.,]+)\s*([kKmMbB])?\s*(?:Followers|followers)',
            r'(?:Followers|followers):\s*([\d.,]+)\s*([kKmMbB])?',
            r'([\d.,]+)\s*([kKmMbB])?\s*abonnés' # French/multilingual common in SERP snippets
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                raw_num = match.group(1).replace(',', '')
                multiplier = match.group(2)
                try:
                    num = float(raw_num)
                    if multiplier:
                        m = multiplier.upper()
                        if m == 'K':
                            num *= 1_000
                        elif m == 'M':
                            num *= 1_000_000
                        elif m == 'B':
                            num *= 1_000_000_000
                    return int(num)
                except ValueError:
                    continue
        return None

    @staticmethod
    def format_followers(followers: Optional[int]) -> str:
        if followers is None:
            return "Not available"
        if followers >= 1_000_000:
            return f"{followers / 1_000_000:.1f}M".replace('.0M', 'M')
        if followers >= 1_000:
            return f"{followers / 1_000:.1f}K".replace('.0K', 'K')
        return f"{followers:,}"

    @staticmethod
    def clean_bio_snippet(snippet: str) -> str:
        if not snippet:
            return ""
        # Remove common search engine boilerplate
        clean = re.sub(r'[\d.,]+[kKmM]?\s*Followers[,\s]*[\d.,]+[kKmM]?\s*Following[,\s]*[\d.,]+[kKmM]?\s*Posts\s*[-–•]?\s*', '', snippet, flags=re.IGNORECASE)
        clean = re.sub(r'See Instagram photos and videos from [^•]+[•]?', '', clean, flags=re.IGNORECASE)
        clean = clean.strip()
        return clean

    @staticmethod
    def evaluate_confidence(
        has_bio: bool,
        has_followers: bool,
        has_region_signal: bool,
        is_direct_profile: bool
    ) -> Tuple[ConfidenceLevel, List[ConfidenceDetail]]:
        details: List[ConfidenceDetail] = []
        
        if is_direct_profile and has_bio and has_followers:
            level = ConfidenceLevel.HIGH
            details.append(ConfidenceDetail(
                field="profile_data",
                level=ConfidenceLevel.HIGH,
                source="Public SERP Index",
                description="Verified handle, complete snippet bio, and indexed follower metrics"
            ))
        elif has_bio or has_followers:
            level = ConfidenceLevel.MEDIUM
            details.append(ConfidenceDetail(
                field="bio_or_metrics",
                level=ConfidenceLevel.MEDIUM,
                source="Search Snippet",
                description="Profile confirmed with partial public snippet signals"
            ))
        else:
            level = ConfidenceLevel.LOW
            details.append(ConfidenceDetail(
                field="handle_only",
                level=ConfidenceLevel.LOW,
                source="Search Context",
                description="Handle identified, but detailed public bio text was unavailable in search snippet"
            ))
            
        if has_region_signal:
            details.append(ConfidenceDetail(
                field="region",
                level=ConfidenceLevel.HIGH if has_bio else ConfidenceLevel.MEDIUM,
                source="Bio / Context Text",
                description="Explicit regional signal detected in profile metadata"
            ))
            
        return level, details
