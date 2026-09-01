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
  const { query, total_found } = response;

  return (
    <div className="results-meta-bar">
      <div>
        <div className="results-meta-title">
          Showing {filteredCount} of {total_found} Publicly Discoverable Profiles
        </div>
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
