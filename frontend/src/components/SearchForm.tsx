import React, { useState } from 'react';
import { Search, X } from 'lucide-react';
import { SearchRequest } from '../types';

interface SearchFormProps {
  onSearch: (request: SearchRequest) => void;
  isLoading: boolean;
}

const REGION_OPTIONS = [
  'India — Any Region',
  'Delhi',
  'Mumbai',
  'Bangalore',
  'Hyderabad',
  'Chennai',
  'Kolkata',
  'Pune',
  'Ahmedabad',
  'Jaipur',
  'Chandigarh',
  'Gurgaon',
  'Noida',
  'Lucknow',
  'Indore',
  'Kochi'
];

const NICHE_OPTIONS = [
  'Fashion',
  'Beauty',
  'Lifestyle',
  'Fitness',
  'Food',
  'Travel',
  'Technology',
  'Gaming',
  'Finance',
  'Music',
  'Photography',
  'Art',
  'Education',
  'Business',
  'Comedy',
  'Sports',
  'Health',
  'Other'
];

const FOLLOWER_OPTIONS = [
  { label: 'Any followers', min: undefined, max: undefined },
  { label: '1K – 10K', min: 1000, max: 10000 },
  { label: '10K – 50K', min: 10000, max: 50000 },
  { label: '50K – 100K', min: 50000, max: 100000 },
  { label: '100K – 500K', min: 100000, max: 500000 },
  { label: '500K+', min: 500000, max: undefined },
  { label: 'Custom range', min: undefined, max: undefined, isCustom: true }
];

export const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
  const [region, setRegion] = useState('Delhi');
  const [niche, setNiche] = useState('Fashion');
  const [followerSelection, setFollowerSelection] = useState('10K – 50K');
  const [customMin, setCustomMin] = useState<number | undefined>(undefined);
  const [customMax, setCustomMax] = useState<number | undefined>(undefined);
  
  const [keywords, setKeywords] = useState<string[]>(['model', 'creator']);
  const [keywordInput, setKeywordInput] = useState('');

  const isCustomRange = followerSelection === 'Custom range';

  const handleAddKeyword = () => {
    const trimmed = keywordInput.trim();
    if (trimmed && !keywords.includes(trimmed)) {
      setKeywords([...keywords, trimmed]);
      setKeywordInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      handleAddKeyword();
    }
  };

  const handleRemoveKeyword = (kwToRemove: string) => {
    setKeywords(keywords.filter((kw) => kw !== kwToRemove));
  };

  const handleApplyQuickExample = (exRegion: string, exNiche: string, exFollowerLabel: string, exKeywords: string[]) => {
    setRegion(exRegion);
    setNiche(exNiche);
    setFollowerSelection(exFollowerLabel);
    setKeywords(exKeywords);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    let minF: number | undefined;
    let maxF: number | undefined;

    if (isCustomRange) {
      minF = customMin;
      maxF = customMax;
    } else {
      const found = FOLLOWER_OPTIONS.find((f) => f.label === followerSelection);
      if (found) {
        minF = found.min;
        maxF = found.max;
      }
    }

    const cleanRegion = region.includes('Any Region') ? undefined : region.trim();

    onSearch({
      region: cleanRegion || undefined,
      niche: niche.trim() || undefined,
      followers_min: minF,
      followers_max: maxF,
      keywords: keywords,
      provider: 'search',
      max_results: 30,
    });
  };

  return (
    <div className="search-card">
      <form onSubmit={handleSubmit}>
        <div className="search-form-grid">
          {/* Region */}
          <div className="input-group">
            <label className="input-label">Region</label>
            <select
              className="app-select"
              value={region}
              onChange={(e) => setRegion(e.target.value)}
            >
              {REGION_OPTIONS.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>

          {/* Niche */}
          <div className="input-group">
            <label className="input-label">Niche</label>
            <select
              className="app-select"
              value={niche}
              onChange={(e) => setNiche(e.target.value)}
            >
              {NICHE_OPTIONS.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
          </div>

          {/* Follower Range (One Dropdown) */}
          <div className="input-group">
            <label className="input-label">Follower Range</label>
            <select
              className="app-select"
              value={followerSelection}
              onChange={(e) => setFollowerSelection(e.target.value)}
            >
              {FOLLOWER_OPTIONS.map((opt) => (
                <option key={opt.label} value={opt.label}>
                  {opt.label}
                </option>
              ))}
            </select>

            {isCustomRange && (
              <div className="custom-followers-row">
                <input
                  type="number"
                  className="app-input"
                  placeholder="Min (e.g. 10000)"
                  value={customMin || ''}
                  onChange={(e) =>
                    setCustomMin(e.target.value ? parseInt(e.target.value) : undefined)
                  }
                />
                <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>to</span>
                <input
                  type="number"
                  className="app-input"
                  placeholder="Max (e.g. 100000)"
                  value={customMax || ''}
                  onChange={(e) =>
                    setCustomMax(e.target.value ? parseInt(e.target.value) : undefined)
                  }
                />
              </div>
            )}
          </div>

          {/* Keywords */}
          <div className="input-group">
            <label className="input-label">Bio Keywords</label>
            <div className="keyword-input-box">
              {keywords.map((kw) => (
                <span key={kw} className="keyword-chip">
                  {kw}
                  <button
                    type="button"
                    className="chip-remove-btn"
                    onClick={() => handleRemoveKeyword(kw)}
                  >
                    <X size={11} />
                  </button>
                </span>
              ))}
              <input
                type="text"
                className="keyword-inline-input"
                placeholder={keywords.length === 0 ? "e.g. model, creator (press Enter)" : "Add keyword..."}
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                onKeyDown={handleKeyDown}
                onBlur={handleAddKeyword}
              />
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="search-footer-row">
          <div className="quick-examples">
            <span>Try:</span>
            <button
              type="button"
              className="quick-example-btn"
              onClick={() =>
                handleApplyQuickExample('Delhi', 'Fashion', '10K – 50K', ['model', 'creator'])
              }
            >
              Delhi fashion creators
            </button>
            <span>·</span>
            <button
              type="button"
              className="quick-example-btn"
              onClick={() =>
                handleApplyQuickExample('Mumbai', 'Beauty', '10K – 50K', ['mua', 'makeup'])
              }
            >
              Mumbai beauty creators
            </button>
            <span>·</span>
            <button
              type="button"
              className="quick-example-btn"
              onClick={() =>
                handleApplyQuickExample('Bangalore', 'Technology', '10K – 50K', ['developer', 'coding'])
              }
            >
              Bangalore tech creators
            </button>
          </div>

          <button type="submit" className="btn-primary-cta" disabled={isLoading}>
            <Search size={15} />
            {isLoading ? 'SEARCHING PUBLIC WEB...' : 'FIND PROFILES'}
          </button>
        </div>
      </form>
    </div>
  );
};
