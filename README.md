# INSCOUT — Public Instagram Profile Discovery & Filtering Engine

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![React](https://img.shields.io/badge/react-18%2B-61dafb)
![FastAPI](https://img.shields.io/badge/fastapi-0.110%2B-009688)

**INSCOUT** is a zero-cost (₹0 MVP) discovery engine designed to discover **real, publicly accessible Instagram profiles** based on user-defined criteria (Region, Niche, Follower Range, Bio Keywords), analyze available public signals, assign relevant tags, calculate a transparent Match Score (0–100), and present the results in an Instagram-inspired dark research interface with RFC4180 CSV export.

---

## 🚀 Key Features

* **Multi-Criteria Public Discovery**:
  * **Region**: Autocomplete for major Indian and global cities (`Delhi`, `Mumbai`, `Bangalore`, `Hyderabad`, `Chennai`, `Kolkata`, `Pune`, `Ahmedabad`, `Jaipur`, `Chandigarh`, `Gurgaon`, `Noida`, `Lucknow`, `Indore`, `Kochi`, etc.).
  * **Niche**: 18+ comprehensive taxonomy categories (`Fashion`, `Beauty`, `Lifestyle`, `Fitness`, `Food`, `Travel`, `Technology`, `Gaming`, `Finance`, `Music`, `Photography`, `Art`, `Education`, `Business`, `Comedy`, `Sports`, `Health`, `Other`).
  * **Follower Range**: Single compact dropdown (`Any followers`, `1K–10K`, `10K–50K`, `50K–100K`, `100K–500K`, `500K+`, `Custom range`).
  * **Bio Keywords**: Interactive chip-based keyword tags with Enter key support.
* **₹0 & Compliant Public Discovery**:
  * Uses multi-strategy public web indexing (DuckDuckGo, Brave public SERP index, Bing public web index) without paid APIs or scraping proxies.
  * Strictly filters non-profile Instagram routes (`explore`, `reels`, `p`, `stories`, `popular`, `channel`, etc.).
* **Transparent Match Scoring (0–100)**:
  * Centralized, configurable weights: Niche (35%), Region (25%), Followers (20%), Keywords (20%).
  * Itemized "Why this score?" breakdown explaining exact score contributions on every profile card.
* **Honest Data Provenance & Integrity**:
  * Zero fake or simulated profiles in production workflows. If 0 profiles match, 0 are returned.
  * Fields not publicly discoverable strictly display as `"Not available"`.
  * Data confidence badges (`High`, `Medium`, `Low`) based on signal sources.
* **Instagram-Inspired Dark UI**:
  * Near-black background (`#000000`), dark charcoal surfaces (`#121212`), subtle grey borders, and tasteful Instagram gradient accents.
  * Progressive disclosure for clean visual scanning.
* **Post-Discovery Filtering & Sorting**:
  * Instant multi-tag, region, and minimum match score filtering.
  * Sorting by Match Score, Follower Count, or Region.
* **1-Click CSV Export**:
  * Formatted RFC4180 CSV download with UTF-8-SIG encoding for seamless Excel / Numbers / Google Sheets compatibility.

---

## 🏗️ System Architecture

```text
User Criteria (Region, Niche, Followers, Keywords)
                      │
                      ▼
  Search Query Generator (Layered Dorks)
                      │
                      ▼
     Public Web Search Discovery Engine
                      │
                      ▼
  Real Candidate Instagram Profiles
                      │
                      ▼
   Profile Normalizer & Confidence Evaluator
                      │
                      ▼
     Rule-Based Deterministic Tagging Engine
                      │
                      ▼
    Transparent Match Scoring Engine (0-100)
                      │
                      ▼
  React TypeScript SaaS UI & RFC4180 CSV Export
```

---

## 📦 Project Structure

```text
INSCOUT/
├── backend/
│   ├── app/
│   │   ├── config.py             # Configurable scoring weights & app settings
│   │   ├── main.py               # FastAPI router endpoints & CORS middleware
│   │   ├── discovery/
│   │   │   ├── base.py           # Abstract Base DiscoveryProvider
│   │   │   ├── search_provider.py# Multi-source public web search provider
│   │   │   ├── mock_provider.py  # Isolated mock provider for unit testing
│   │   │   └── engine.py         # Discovery coordinator
│   │   ├── models/
│   │   │   ├── profile.py        # DiscoveredProfile, DataConfidence models
│   │   │   ├── search.py         # SearchRequest & SearchFilterParams models
│   │   │   └── response.py       # SearchResponse, ExportResponse, HealthResponse
│   │   ├── services/
│   │   │   ├── query_generator.py# Layered search query builder
│   │   │   ├── normalizer.py     # Username cleaner, follower parser & confidence
│   │   │   ├── tagger.py         # Deterministic taxonomy & regex tagger
│   │   │   ├── scorer.py         # Multi-factor Match Score calculator
│   │   │   └── exporter.py       # RFC4180 CSV generator
│   │   └── storage/
│   │       └── session_store.py  # Fast in-memory session cache
│   ├── requirements.txt
│   └── tests/
│       ├── test_engine.py        # Unit test suite
│       ├── verify_e2e.py         # End-to-end API integration tests
│       └── verify_real_discovery_report.py # Live search discovery audit
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts         # Typed API client
│   │   ├── components/
│   │   │   ├── Header.tsx        # Minimal brand header with status badge
│   │   │   ├── SearchForm.tsx    # Region, niche, follower dropdown, keywords
│   │   │   ├── FiltersBar.tsx    # Compact filter dropdowns & sorting
│   │   │   ├── ProfileCard.tsx   # Progressive disclosure profile card
│   │   │   ├── ResultsSummary.tsx# Search metrics & CSV export trigger
│   │   │   └── Common/
│   │   │       ├── EmptyState.tsx
│   │   │       └── LoadingSkeleton.tsx
│   │   ├── types/
│   │   │   └── index.ts          # Shared TypeScript definitions
│   │   ├── App.tsx               # Root layout & state manager
│   │   ├── index.css             # Instagram-inspired dark theme CSS system
│   │   └── main.tsx              # React entrypoint
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── .gitignore
└── README.md
```

---

## ⚡ Getting Started

### Prerequisites
* **Python 3.12+**
* **Node.js 18+** and **npm**

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend will be live at `http://127.0.0.1:8000`. API documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend

# Install packages
npm install

# Start Vite development server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Running Tests

### Backend Unit Tests
```bash
cd backend
python -m pytest tests/test_engine.py
```

### End-to-End Live Discovery Audit
```bash
cd backend
python -m tests.verify_real_discovery_report
```

### Frontend Build Validation
```bash
cd frontend
npm run build
```

---

## 📡 API Reference

### `POST /api/search`
Executes real public web discovery against user criteria.

**Request Body:**
```json
{
  "region": "Delhi",
  "niche": "Fashion",
  "followers_min": 10000,
  "followers_max": 100000,
  "keywords": ["model", "creator"],
  "provider": "search",
  "max_results": 30
}
```

### `GET /api/results/{search_id}`
Retrieves cached search session results.

### `GET /api/profile/{username}`
Retrieves detailed metadata for a discovered profile handle.

### `GET /api/export/{search_id}?format=csv`
Downloads an RFC4180 CSV file with UTF-8-SIG encoding containing all discovered profiles.

### `GET /api/health`
Health check endpoint returning service status and version.

---

## 📄 License

MIT License. Designed and built as a transparent, zero-cost public discovery research tool.
