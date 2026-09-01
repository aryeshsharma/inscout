import React from 'react';
import { Download } from 'lucide-react';
import { SearchResponse } from '../types';

interface ResultsSummaryProps {
  response: SearchResponse;
  filteredCount: number;
  onExportCsv: () => void;
  isExporting: boolean;
}

export const ResultsSummary: React.FC<ResultsSummaryProps> = ({
  response,
  filteredCount,
  onExportCsv,
  isExporting,
}) => {
  const { query, total_found, candidates_discovered, profiles_verified, profiles_matched } = response;

  return (
    <div className="results-meta-bar">
      <div>
        <div className="results-meta-title">
          Showing {filteredCount} of {total_found} Publicly Discoverable Profiles
        </div>

        {/* Discovery Pipeline Transparency Counters */}
        {candidates_discovered > 0 && (
          <div style={{ fontSize: '0.76rem', color: '#38bdf8', marginTop: '2px', fontWeight: 500 }}>
            {candidates_discovered} candidates discovered · {profiles_verified} verified · {profiles_matched} match your criteria
          </div>
        )}

        <div className="results-criteria-text">
          <span>Criteria: </span>
          {query.region ? <strong>{query.region}</strong> : 'All Regions'} ·{' '}
          {query.niche ? <strong>{query.niche}</strong> : 'All Niches'}
          {(query.followers_min || query.followers_max) && (
            <span>
              {' '}· Followers: {query.followers_min ? query.followers_min.toLocaleString() : '0'} –{' '}
              {query.followers_max ? query.followers_max.toLocaleString() : '500K+'}
            </span>
          )}
          {query.keywords && query.keywords.length > 0 && (
            <span> · Keywords: {query.keywords.join(', ')}</span>
          )}
        </div>
      </div>

      <div>
        <button
          type="button"
          className="export-csv-btn"
          onClick={onExportCsv}
          disabled={isExporting || total_found === 0}
          title="Export discovered profiles to CSV"
        >
          <Download size={13} />
          {isExporting ? 'Exporting...' : 'Export CSV'}
        </button>
      </div>
    </div>
  );
};
