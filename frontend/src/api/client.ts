import { SearchRequest, SearchResponse, DiscoveredProfile } from '../types';

const API_BASE = '/api';

export class ApiClient {
  
  static async searchProfiles(request: SearchRequest): Promise<SearchResponse> {
    const response = await fetch(`${API_BASE}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Network request failed' }));
      throw new Error(errorData.detail || `Search failed with HTTP ${response.status}`);
    }

    return response.json();
  }

  static async getResults(searchId: string): Promise<SearchResponse> {
    const response = await fetch(`${API_BASE}/results/${encodeURIComponent(searchId)}`);
    if (!response.ok) {
      throw new Error(`Failed to load search results: HTTP ${response.status}`);
    }
    return response.json();
  }

  static async getProfile(username: string): Promise<DiscoveredProfile> {
    const response = await fetch(`${API_BASE}/profile/${encodeURIComponent(username)}`);
    if (!response.ok) {
      throw new Error(`Failed to load profile details for @${username}`);
    }
    return response.json();
  }

  static async downloadCsv(searchId: string, filename: string): Promise<void> {
    const response = await fetch(`${API_BASE}/export/${encodeURIComponent(searchId)}?format=csv`);
    if (!response.ok) {
      throw new Error('Failed to generate CSV export');
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);
    window.URL.revokeObjectURL(url);
  }

  static async checkHealth(): Promise<{ status: string; version: string; active_providers: string[] }> {
    const response = await fetch(`${API_BASE}/health`);
    if (!response.ok) {
      throw new Error('Backend health check failed');
    }
    return response.json();
  }
}
