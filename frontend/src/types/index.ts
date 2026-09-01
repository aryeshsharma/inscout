export type ConfidenceLevel = 'High' | 'Medium' | 'Low';

export interface ConfidenceDetail {
  field: string;
  level: ConfidenceLevel;
  source: string;
  description?: string;
}

export interface MatchReason {
  criterion: string;
  matched: boolean;
  description: string;
  score_contribution: number;
}

export interface DiscoveredProfile {
  username: string;
  profile_url: string;
  display_name?: string | null;
  bio?: string | null;
  followers?: number | null;
  followers_formatted?: string | null;
  region?: string | null;
  tags: string[];
  matched_keywords: string[];
  match_score: number;
  match_reasons: MatchReason[];
  data_confidence: ConfidenceLevel;
  confidence_details: ConfidenceDetail[];
  is_demo: boolean;
  profile_image?: string | null;
  following?: number | null;
  posts?: number | null;
  engagement_rate?: number | null;
  category?: string | null;
  discovery_source?: string;
  source_query?: string | null;
}

export interface SearchRequest {
  region?: string;
  niche?: string;
  followers_min?: number;
  followers_max?: number;
  keywords: string[];
  provider?: string;
  max_results?: number;
}

export interface SearchResponse {
  search_id: string;
  query: SearchRequest;
  total_found: number;
  candidates_discovered: number;
  profiles_verified: number;
  profiles_matched: number;
  provider_used: string;
  is_demo: boolean;
  profiles: DiscoveredProfile[];
  available_tags: string[];
  available_regions: string[];
  execution_time_ms: number;
  warning?: string | null;
}

export interface FilterState {
  selectedTags: string[];
  selectedRegion: string;
  minScore: number;
  followerPreset: string;
  customFollowersMin?: number;
  customFollowersMax?: number;
  sortBy: 'score' | 'score_asc' | 'followers_desc' | 'followers_asc' | 'region';
  searchQueryText: string;
}
