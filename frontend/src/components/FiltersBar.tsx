import React from 'react';
import { FilterState } from '../types';

interface FiltersBarProps {
  availableTags: string[];
  availableRegions: string[];
  filterState: FilterState;
  onFilterChange: (newState: FilterState) => void;
  onResetFilters: () => void;
  totalFiltered: number;
  totalFound: number;
}

export const FiltersBar: React.FC<FiltersBarProps> = ({
  availableTags,
  availableRegions,
  filterState,
  onFilterChange,
  onResetFilters,
  totalFiltered,
  totalFound,
}) => {
  const hasActiveFilters =
    filterState.selectedTags.length > 0 ||
    filterState.selectedRegion !== '' ||
    filterState.minScore > 0;

  return (
    <div className="compact-filters-bar">
      {/* Tag Dropdown */}
      {availableTags.length > 0 && (
        <select
          className="filter-select"
          value={filterState.selectedTags[0] || ''}
          onChange={(e) => {
            const val = e.target.value;
            onFilterChange({
              ...filterState,
              selectedTags: val ? [val] : [],
            });
          }}
        >
          <option value="">All Tags ({availableTags.length})</option>
          {availableTags.map((tag) => (
            <option key={tag} value={tag}>
              Tag: {tag}
            </option>
          ))}
        </select>
      )}

      {/* Region Dropdown */}
      {availableRegions.length > 1 && (
        <select
          className="filter-select"
          value={filterState.selectedRegion}
          onChange={(e) =>
            onFilterChange({
              ...filterState,
              selectedRegion: e.target.value,
            })
          }
        >
          <option value="">All Detected Regions</option>
          {availableRegions.map((reg) => (
            <option key={reg} value={reg}>
              Region: {reg}
            </option>
          ))}
        </select>
      )}

      {/* Min Match Score */}
      <select
        className="filter-select"
        value={filterState.minScore || 0}
        onChange={(e) =>
          onFilterChange({
            ...filterState,
            minScore: parseInt(e.target.value) || 0,
          })
        }
      >
        <option value={0}>Any Match Score</option>
        <option value={70}>70+ Match</option>
        <option value={80}>80+ Match</option>
        <option value={90}>90+ Match</option>
      </select>

      {/* Sort Dropdown */}
      <select
        className="filter-select"
        value={filterState.sortBy}
        onChange={(e) =>
          onFilterChange({
            ...filterState,
            sortBy: e.target.value as FilterState['sortBy'],
          })
        }
      >
        <option value="score">Highest Match Score</option>
        <option value="score_asc">Lowest Match Score</option>
        <option value="followers_desc">Highest Followers</option>
        <option value="followers_asc">Lowest Followers</option>
      </select>

      {/* Reset button if active */}
      {hasActiveFilters && (
        <button
          type="button"
          className="clear-filters-btn"
          onClick={onResetFilters}
        >
          Reset Filters ({totalFiltered}/{totalFound})
        </button>
      )}
    </div>
  );
};
