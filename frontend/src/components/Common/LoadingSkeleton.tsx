import React from 'react';

export const LoadingSkeleton: React.FC = () => {
  return (
    <div className="profiles-list">
      {[1, 2, 3, 4, 5].map((i) => (
        <div key={i} className="skeleton-card" />
      ))}
    </div>
  );
};
