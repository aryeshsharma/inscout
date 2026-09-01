import React, { useState, useEffect, useMemo } from 'react';
import { Header } from './components/Header';
import { SearchForm } from './components/SearchForm';
import { FiltersBar } from './components/FiltersBar';
import { ResultsSummary } from './components/ResultsSummary';
import { ProfileCard } from './components/ProfileCard';
import { LoadingSkeleton } from './components/Common/LoadingSkeleton';
import { EmptyState } from './components/Common/EmptyState';
import { ApiClient } from './api/client';
import { SearchRequest, SearchResponse, FilterState } from './types';
import { AlertCircle } from 'lucide-react';

export const App: React.FC = () => {
  const [apiConnected, setApiConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null);

  // Post-search filter & sorting state
  const [filterState, setFilterState] = useState<FilterState>({
    selectedTags: [],
    selectedRegion: '',
    minScore: 0,
    followerPreset: 'All',
    sortBy: 'score',
    searchQueryText: '',
  });

  // Initial Health Check and default initial live search
  useEffect(() => {
    const initApp = async () => {
      try {
        await ApiClient.checkHealth();
        setApiConnected(true);
        // Execute initial live discovery search
        handleSearch({
          region: 'Delhi',
          niche: 'Fashion',
          followers_min: 10000,
          followers_max: 50000,
          keywords: ['model', 'creator'],
          provider: 'search',
          max_results: 30,
        });
      } catch (err) {
        console.error('API connection check failed:', err);
        setApiConnected(false);
        setErrorMessage('Could not connect to INSCOUT backend. Please ensure the backend server is running.');
      }
    };
    initApp();
  }, []);

  const handleSearch = async (request: SearchRequest) => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const response = await ApiClient.searchProfiles({
        ...request,
        provider: 'search',
      });
      setSearchResponse(response);
      // Reset post-filters on fresh search
      setFilterState({
        selectedTags: [],
        selectedRegion: '',
        minScore: 0,
        followerPreset: 'All',
        sortBy: 'score',
        searchQueryText: '',
      });
    } catch (err: any) {
      setErrorMessage(err.message || 'Live public discovery is currently unavailable.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportCsv = async () => {
    if (!searchResponse) return;
    setIsExporting(true);
    try {
      const filename = `inscout_${searchResponse.query.niche || 'profiles'}_${searchResponse.search_id.slice(0, 8)}.csv`;
      await ApiClient.downloadCsv(searchResponse.search_id, filename);
    } catch (err: any) {
      alert(`Export failed: ${err.message}`);
    } finally {
      setIsExporting(false);
    }
  };

  const handleResetFilters = () => {
    setFilterState({
      selectedTags: [],
      selectedRegion: '',
      minScore: 0,
      followerPreset: 'All',
      sortBy: 'score',
      searchQueryText: '',
    });
  };

  // Filter and sort candidate profiles client-side for rapid response
  const filteredProfiles = useMemo(() => {
    if (!searchResponse) return [];
    let list = [...searchResponse.profiles];

    // Filter by selected tags
    if (filterState.selectedTags.length > 0) {
      list = list.filter((p) =>
        filterState.selectedTags.every((t) => p.tags.includes(t))
      );
    }

    // Filter by region
    if (filterState.selectedRegion) {
      list = list.filter(
        (p) => p.region?.toLowerCase() === filterState.selectedRegion.toLowerCase()
      );
    }

    // Filter by min score
    if (filterState.minScore > 0) {
      list = list.filter((p) => p.match_score >= filterState.minScore);
    }

    // Sort
    list.sort((a, b) => {
      switch (filterState.sortBy) {
        case 'score':
          return b.match_score - a.match_score;
        case 'score_asc':
          return a.match_score - b.match_score;
        case 'followers_desc':
          return (b.followers || 0) - (a.followers || 0);
        case 'followers_asc':
          return (a.followers || 0) - (b.followers || 0);
        case 'region':
          return (a.region || '').localeCompare(b.region || '');
        default:
          return b.match_score - a.match_score;
      }
    });

    return list;
  }, [searchResponse, filterState]);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'var(--bg-app)' }}>
      <Header apiConnected={apiConnected} />

      <main className="app-container">
        {/* Error Alert Banner */}
        {errorMessage && (
          <div
            style={{
              background: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid rgba(239, 68, 68, 0.25)',
              borderRadius: 'var(--radius-md)',
              padding: '12px 16px',
              marginTop: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              color: '#f87171',
              fontSize: '0.84rem',
            }}
          >
            <AlertCircle size={16} />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Warning from backend */}
        {searchResponse?.warning && (
          <div
            style={{
              background: '#141414',
              border: '1px solid #262626',
              borderRadius: 'var(--radius-md)',
              padding: '12px 16px',
              marginTop: '20px',
              color: '#a8a8a8',
              fontSize: '0.84rem',
            }}
          >
            {searchResponse.warning}
          </div>
        )}

        {/* Primary Search Area */}
        <SearchForm onSearch={handleSearch} isLoading={isLoading} />

        {/* Loading State */}
        {isLoading && <LoadingSkeleton />}

        {/* Results Section */}
        {!isLoading && searchResponse && (
          <div>
            <ResultsSummary
              response={searchResponse}
              filteredCount={filteredProfiles.length}
              onExportCsv={handleExportCsv}
              isExporting={isExporting}
            />

            {/* Compact Filters */}
            <FiltersBar
              availableTags={searchResponse.available_tags}
              availableRegions={searchResponse.available_regions}
              filterState={filterState}
              onFilterChange={setFilterState}
              onResetFilters={handleResetFilters}
              totalFiltered={filteredProfiles.length}
              totalFound={searchResponse.total_found}
            />

            {/* Discovered Profiles List */}
            {filteredProfiles.length > 0 ? (
              <div className="profiles-list">
                {filteredProfiles.map((profile) => (
                  <ProfileCard key={profile.username} profile={profile} />
                ))}
              </div>
            ) : (
              <EmptyState
                title={searchResponse.total_found === 0 ? "No public profiles found." : "No profiles match active filters."}
                message={searchResponse.total_found === 0 ? "Try broadening your region, niche, follower range, or keywords." : "Try adjusting your tag, score, or sorting filters above."}
                onReset={searchResponse.total_found > 0 ? handleResetFilters : undefined}
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
