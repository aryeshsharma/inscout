# INSCOUT — Public Instagram Profile Discovery & Qualification Engine

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![React](https://img.shields.io/badge/react-18%2B-61dafb)
![FastAPI](https://img.shields.io/badge/fastapi-0.110%2B-009688)

**INSCOUT** is a zero-cost (₹0 MVP) public discovery engine designed to discover **real, publicly accessible Instagram creators** based on user-defined criteria (Region, Niche, Follower Range, Bio Keywords), extract available public signals, apply strict evidence-based qualification filters, calculate a transparent Match Score (0–100), and present results in an Instagram-inspired dark research interface with RFC4180 CSV export.

---

## 🚀 Key Features

* **Real Data Only**:
  * Pure live discovery from publicly indexed Instagram profiles.
  * Zero synthetic, simulated, or demo profiles in live search responses.
  * Strict signal verification: if a field is not discoverable from public snippets, it is explicitly marked as `"Not available"`.
* **Zero Username-Location Bias**:
  * A city name in a username (e.g. `@delhi_creator`) is **never** accepted as proof of location.
  * Geographic qualification is strictly evaluated from bio text and indexed location evidence (`HIGH` or `MEDIUM` confidence).
* **Strict Hard Eligibility Filters**:
  * **Follower Range**: Strict hard filter (`min <= followers <= max`). Unknown follower counts are rejected when a range is requested.
  * **Region**: Strict bio-verified location matching.
  * **Niche**: Strict semantic taxonomy verification across 17+ niches (`Fashion`, `Beauty`, `Lifestyle`, `Travel`, `Technology`, `Fitness`, `Food`, `Gaming`, `Finance`, `Music`, `Photography`, `Art`, `Education`, `Business`, `Comedy`, `Sports`, `Health`).
* **Transparent Multi-Factor Match Scoring (0–100)**:
  * Geographic Relevance: 0–30 pts (Bio-verified evidence only).
  * Niche Relevance: 0–30 pts (Semantic taxonomy match).
  * Bio Keyword Match: 0–20 pts (Normalized concept matching).
  * Context & Collaboration Signals: 0–10 pts (PR/collab intent, rich bio).
  * Data Confidence: 0–10 pts (Signal completeness).
  * Follower count is a **0% score weight** (hard filter gate only).
* **₹0 Cost & Platform Compliance**:
  * Zero paid scraping APIs, commercial databases, or proxies.
  * Operates strictly on public web indexing without bypassing platform restrictions or accessing private profiles.
* **1-Click RFC4180 CSV Export**:
  * UTF-8-SIG encoded CSV export with complete provenance, match reasons, and data confidence levels.

---

## 🏗️ System Architecture

```text
User Criteria (Region, Niche, Follower Range, Keywords)
                      │
                      ▼
   Dynamic Semantic Query Expansion (30-50+ Anti-Bias Queries)
                      │
                      ▼
       Multi-Engine Live Public SERP Discovery
                      │
                      ▼
   Candidate Normalization & Route Deduplication
                      │
                      ▼
   [HARD FILTER 1] Follower Range (min <= f <= max; unknown rejected)
                      │
                      ▼
   [HARD FILTER 2] Region Verification (Bio Evidence Only, 0% Handle Credit)
                      │
                      ▼
   [HARD FILTER 3] Semantic Niche Qualification
                      │
                      ▼
   Transparent Multi-Factor Match Scoring (0-100)
                      │
                      ▼
   React TypeScript Dark SaaS UI & RFC4180 CSV Export
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
│   │   │   ├── search_provider.py# Multi-source live public search provider
│   │   │   ├── mock_provider.py  # Isolated mock provider for unit testing
│   │   │   ├── meta_provider.py  # Optional Meta Business Discovery provider
│   │   │   └── engine.py         # Discovery coordinator
│   │   ├── models/
│   │   │   ├── profile.py        # DiscoveredProfile, DataConfidence models
│   │   │   ├── search.py         # SearchRequest & SearchFilterParams models
│   │   │   └── response.py       # SearchResponse, ExportResponse, HealthResponse
│   │   ├── services/
│   │   │   ├── query_expansion.py# Multi-angle anti-bias query builder
│   │   │   ├── normalizer.py     # Username cleaner, follower parser & confidence
│   │   │   ├── tagger.py         # Deterministic taxonomy & regex tagger
│   │   │   ├── scorer.py         # Multi-factor Match Score calculator
│   │   │   └── exporter.py       # RFC4180 CSV generator
│   │   └── storage/
│   │       └── session_store.py  # Fast in-memory session cache
│   ├── requirements.txt
│   └── tests/
│       ├── test_candidate_pipeline.py    # Pipeline & anti-bias tests
│       ├── test_engine.py                # Engine unit tests
│       ├── test_follower_filter.py       # Strict boundary tests
│       ├── test_full_production_suite.py # 15-category audit test suite
│       ├── test_query_expansion.py       # Query expansion tests
│       └── verify_real_discovery_report.py# 6-scenario forensic benchmark
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

The backend is live at `http://127.0.0.1:8000`. API docs available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Running Tests

### Full Backend Test Suite (37 Tests)
```bash
cd backend
python -m pytest
```

### Frontend Build Validation
```bash
cd frontend
npm run build
```

---

## 📡 API Reference

### `POST /api/search`
Executes live public web discovery against user criteria.

**Request Body:**
```json
{
  "region": "Delhi",
  "niche": "Fashion",
  "followers_min": 10000,
  "followers_max": 100000,
  "keywords": ["model", "creator"],
  "provider": "search",
  "max_results": 100
}
```

### `GET /api/results/{search_id}`
Retrieves cached search session results.

### `GET /api/profile/{username}`
Retrieves detailed metadata for a discovered profile handle.

### `GET /api/export/{search_id}?format=csv`
Downloads an RFC4180 CSV file with UTF-8-SIG encoding.

### `GET /api/health`
Health check endpoint returning service status and active providers.

---

## 📋 Data Source & Coverage Transparency

INSCOUT strictly adheres to a ₹0, legitimate public discovery paradigm:
1. **Public Web SERP Indexing**: Discovers creators indexed by search engines. This provides legitimate public discovery without accessing private profiles or violating platform terms.
2. **Coverage Scope**: Public search engine indexes index a fraction of Instagram's total user base. If search engines rate-limit requests or index few matching bios for specific granular niches, INSCOUT returns only verified matches and never fabricates mock profiles.

---

## 📄 License

MIT License. Designed and built as a transparent, zero-cost public discovery research tool.
