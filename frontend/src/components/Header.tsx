import React from 'react';

interface HeaderProps {
  apiConnected: boolean;
}

export const Header: React.FC<HeaderProps> = ({ apiConnected }) => {
  return (
    <header className="header-wrapper">
      <div className="header-content">
        <div className="brand-section">
          <div className="brand-logo-icon">
            <span>IN</span>
          </div>
          <div>
            <div className="brand-title">INSCOUT</div>
            <div className="brand-tagline">Instagram Profile Discovery Engine</div>
          </div>
        </div>

        <div>
          <div className="status-badge">
            <span className={`status-dot ${apiConnected ? 'online' : 'offline'}`} />
            {apiConnected ? 'LIVE DISCOVERY READY' : 'SEARCH UNAVAILABLE'}
          </div>
        </div>
      </div>
    </header>
  );
};
