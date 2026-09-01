import logging
from typing import Optional, Dict, Any
import httpx

from app.models.profile import DiscoveredProfile, ConfidenceLevel, ConfidenceDetail

logger = logging.getLogger("inscout.meta_provider")

class MetaInstagramProvider:
    """
    Official Meta Instagram Graph API / Business Discovery Provider.
    
    API CAPABILITY AUDIT (Section 14 & 29):
    --------------------------------------
    1. Authentication: Requires Meta App Review, Facebook Login, and a linked Instagram
       Business or Creator Account with 'instagram_basic' and 'pages_show_list' permissions.
    2. Discovery Limitations: Meta Graph API does NOT support open-ended discovery/search
       of arbitrary users by location, niche, or follower range. There is no public user
       directory search endpoint in Meta Graph API.
    3. Enrichment Capability: The 'Business Discovery API' allows looking up public metrics
       (followers, media count, bio, profile picture) for an ALREADY KNOWN professional username.
       Endpoint: GET https://graph.facebook.com/v19.0/{ig-user-id}?fields=business_discovery.username({target_username}){followers_count,media_count,biography,profile_picture_url}
    4. ₹0 MVP Behavior: When no access token is configured, this provider operates in passive mode
       without blocking open public web discovery.
    """

    def __init__(self, access_token: Optional[str] = None, ig_user_id: Optional[str] = None):
        self.access_token = access_token
        self.ig_user_id = ig_user_id
        self.base_url = "https://graph.facebook.com/v19.0"

    @property
    def is_configured(self) -> bool:
        return bool(self.access_token and self.ig_user_id)

    async def enrich_profile(self, profile: DiscoveredProfile) -> DiscoveredProfile:
        """
        Enriches a discovered Instagram business profile via Meta Business Discovery API
        if valid API credentials are provided.
        """
        if not self.is_configured:
            return profile

        try:
            url = f"{self.base_url}/{self.ig_user_id}"
            params = {
                "fields": f"business_discovery.username({profile.username}){{followers_count,media_count,biography,profile_picture_url,name}}",
                "access_token": self.access_token
            }
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json().get("business_discovery", {})
                    if "followers_count" in data:
                        profile.followers = data["followers_count"]
                        profile.followers_formatted = f"{profile.followers:,}"
                    if "biography" in data and not profile.bio:
                        profile.bio = data["biography"]
                    if "profile_picture_url" in data and not profile.profile_image:
                        profile.profile_image = data["profile_picture_url"]
                    if "name" in data and not profile.display_name:
                        profile.display_name = data["name"]
                    
                    profile.data_confidence = ConfidenceLevel.HIGH
                    profile.confidence_details.append(
                        ConfidenceDetail(
                            field="all_fields",
                            level=ConfidenceLevel.HIGH,
                            source="Meta Official Graph API (Business Discovery)"
                        )
                    )
        except Exception as e:
            logger.debug(f"Meta Graph API enrichment skipped for @{profile.username}: {e}")

        return profile
