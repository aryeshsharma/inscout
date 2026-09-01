import React from 'react';
import { SearchX } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  message?: string;
  onReset?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No public profiles found.',
  message = 'Try broadening your region, niche, follower range, or keywords.',
  onReset,
}) => {
  return (
    <div className="empty-results-box">
      <SearchX size={36} color="#737373" />
      <div className="empty-title">{title}</div>
      <p className="empty-subtitle">{message}</p>
      {onReset && (
        <button
          type="button"
          className="export-csv-btn"
          onClick={onReset}
          style={{ marginTop: '8px' }}
        >
          Reset Filters
        </button>
      )}
    </div>
  );
};
