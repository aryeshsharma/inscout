import React, { useState } from 'react';
import { ExternalLink, ChevronDown, ChevronUp, Check, X } from 'lucide-react';
import { DiscoveredProfile } from '../types';

interface ProfileCardProps {
  profile: DiscoveredProfile;
}

export const ProfileCard: React.FC<ProfileCardProps> = ({ profile }) => {
  const [showBreakdown, setShowBreakdown] = useState(false);

  const initialLetter = (profile.display_name || profile.username || '?')
    .charAt(0)
    .toUpperCase();

  const followersDisplay = profile.followers_formatted || (profile.followers ? profile.followers.toLocaleString() : 'Not available');
  const regionDisplay = profile.region || 'Not available';

  return (
    <div className="profile-card">
      <div className="profile-card-header">
        <div className="profile-identity-group">
          {profile.profile_image ? (
            <img
              src={profile.profile_image}
              alt={profile.username}
              className="avatar-placeholder"
              onError={(e) => {
                (e.target as HTMLElement).style.display = 'none';
              }}
            />
          ) : (
            <div className="avatar-placeholder">{initialLetter}</div>
          )}

          <div className="profile-names">
            <a
              href={profile.profile_url}
              target="_blank"
              rel="noopener noreferrer"
              className="profile-handle"
            >
              @{profile.username}
            </a>

            <div className="profile-display-name">
              {profile.display_name || 'Instagram Creator'}
            </div>

            <div className="profile-stats-line">
              <strong>{followersDisplay} followers</strong> · {regionDisplay}
            </div>
          </div>
        </div>

        {/* Match Score Badge */}
        <div className="match-score-badge">
          <span className="score-gradient-text">{profile.match_score}</span>
          <span>Match</span>
        </div>
      </div>

      {/* Bio excerpt if available */}
      {profile.bio && <div className="profile-bio">{profile.bio}</div>}

      {/* Tags line */}
      {profile.tags && profile.tags.length > 0 && (
        <div className="profile-tags-inline">
          {profile.tags.map((tag) => (
            <span key={tag} className="tag-inline-item">
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Card Footer: Toggle and External Link */}
      <div className="profile-card-footer">
        <button
          type="button"
          className="score-toggle-btn"
          onClick={() => setShowBreakdown(!showBreakdown)}
        >
          Why this score {showBreakdown ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
        </button>

        <a
          href={profile.profile_url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-open-ig"
        >
          <ExternalLink size={12} />
          Open Instagram
        </a>
      </div>

      {/* Progressive Disclosure: Match Reasons */}
      {showBreakdown && (
        <div className="score-breakdown-box">
          <div className="breakdown-title">Match Score Explanation ({profile.match_score}/100)</div>
          <ul className="breakdown-list">
            {profile.match_reasons.map((reason, idx) => (
              <li
                key={idx}
                className={`breakdown-item ${reason.matched ? 'matched' : ''}`}
              >
                {reason.matched ? (
                  <Check size={13} className="breakdown-icon-check" />
                ) : (
                  <X size={13} className="breakdown-icon-cross" />
                )}
                <span>
                  <strong>{reason.criterion}:</strong> {reason.description}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
