# GÉODIA / SentinelCare GC — Implementation Plan

## Overview

Build a production-grade AI-assisted preventive maintenance platform for 19 reinforced concrete structures at OCP Jorf Lasfar (marine/chemical environment). The system centralizes asset data, computes priority indices, integrates environmental and InSAR layers, estimates pathology probabilities, generates maintenance plans, and exports inspection dossiers.

**Key decisions:**
- **Stack:** FastAPI + React 18/TypeScript + PostgreSQL (no Docker)
- **Data:** Simulated seed data, clearly flagged `SIMULÉ`
- **API integrations:** Importers built but using simulated data until accounts are set up
- **UI language:** French
- **Auth:** Skipped for V1 prototype
- **Deployment:** Local development (no containerization)

---

## User Review Required

> [!IMPORTANT]
> **PostgreSQL setup**: You'll need PostgreSQL installed locally. I'll configure the app to connect to a local instance. Please confirm:
> - Do you already have PostgreSQL installed?
> - If yes, what port is it running on (default 5432)?
> - Preferred database name? (I'll default to `geodia`)

> [!IMPORTANT]
> **Node.js & Python**: The project requires both Node.js (≥18) and Python (≥3.11). Please confirm these are installed.

> [!WARNING]
> **No Docker** — the backend and frontend must be started separately during development (`uvicorn` for FastAPI, `npm run dev` for React). I'll provide scripts to make this easy.

---

## Open Questions

> [!IMPORTANT]
> **Map tiles:** The spec mentions OpenStreetMap or ESRI tiles. Should I use OpenStreetMap (free, no key) or do you have an ESRI API key? I'll default to **OpenStreetMap + MapLibre GL JS**.

> [!NOTE]
> **Photo storage:** For inspection photos, should I store them as local files on disk (in a `uploads/` directory) or would you prefer a different approach? Local file storage is simplest for V1.

---

## Repository Structure

```
d:\Github\GEODIA\
├── backend/                        # FastAPI Python backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entrypoint + CORS config
│   │   ├── config.py               # Settings (DB URL, paths, etc.)
│   │   ├── database.py             # SQLAlchemy engine + session
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── ouvrage.py
│   │   │   ├── pathologie.py
│   │   │   ├── inspection.py
│   │   │   ├── observation.py
│   │   │   ├── env_timeseries.py
│   │   │   ├── insar_point.py
│   │   │   ├── proba.py
│   │   │   ├── action.py
│   │   │   └── scenario.py
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── ouvrage.py
│   │   │   ├── inspection.py
│   │   │   ├── proba.py
│   │   │   ├── environment.py
│   │   │   ├── insar.py
│   │   │   ├── maintenance.py
│   │   │   └── scenario.py
│   │   ├── routers/                # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── assets.py           # GET /assets, GET /asset/{id}
│   │   │   ├── inspections.py      # POST /inspection, GET /inspections
│   │   │   ├── imports.py          # POST /import/env, /import/insar
│   │   │   ├── compute.py          # POST /compute/proba, /compute/optimize
│   │   │   ├── reports.py          # GET /report/pdf/{id}, /report/excel/{id}
│   │   │   ├── maintenance.py      # GET /maintenance/plan
│   │   │   └── alerts.py           # GET /alerts
│   │   ├── core/                   # Business logic (pure functions)
│   │   │   ├── __init__.py
│   │   │   ├── indices.py          # ICF, IVP, IPD, IED, IAE, IAD, IPM
│   │   │   ├── model_proba.py      # Logistic model P1–P12
│   │   │   ├── insar_pipeline.py   # Descriptors, DBSCAN, IsoForest, consensus
│   │   │   ├── optimizer.py        # PuLP budget optimization
│   │   │   └── alerts.py           # Alert rule engine
│   │   ├── importers/              # Data importers (API + CSV)
│   │   │   ├── __init__.py
│   │   │   ├── nasa_power.py
│   │   │   ├── era5.py
│   │   │   ├── cams.py
│   │   │   ├── sentinel2.py
│   │   │   └── insar_csv.py
│   │   └── exporters/              # PDF + Excel generation
│   │       ├── __init__.py
│   │       ├── pdf_report.py
│   │       └── excel_export.py
│   ├── data/
│   │   ├── seed/                   # Seed CSV files
│   │   │   ├── ouvrages.csv
│   │   │   ├── pathologies.csv
│   │   │   ├── p0_initial.csv
│   │   │   ├── actions_maintenance.csv
│   │   │   └── inspections_template.csv
│   │   └── simulated/              # Simulated data (flagged SIMULÉ)
│   │       ├── env_timeseries_sim.csv
│   │       └── insar_points_sim.csv
│   ├── scripts/
│   │   ├── seed_db.py              # Load seed data into PostgreSQL
│   │   └── generate_simulated.py   # Generate simulated env/InSAR data
│   ├── uploads/                    # Inspection photo storage
│   ├── tests/
│   │   ├── test_indices.py
│   │   ├── test_proba.py
│   │   ├── test_insar.py
│   │   ├── test_optimizer.py
│   │   └── test_api.py
│   ├── alembic/                    # Database migrations
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── versions/
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/                       # React 18 + TypeScript + Vite
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx                 # Router + layout shell
│   │   ├── index.css               # Global design system (CSS custom props)
│   │   ├── api/                    # API client (fetch wrappers)
│   │   │   ├── client.ts
│   │   │   ├── assets.ts
│   │   │   ├── inspections.ts
│   │   │   ├── environment.ts
│   │   │   ├── insar.ts
│   │   │   ├── maintenance.ts
│   │   │   └── reports.ts
│   │   ├── components/             # Reusable UI components
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── PageContainer.tsx
│   │   │   ├── ui/
│   │   │   │   ├── KPICard.tsx
│   │   │   │   ├── DataTable.tsx
│   │   │   │   ├── StatusBadge.tsx
│   │   │   │   ├── AlertCard.tsx
│   │   │   │   └── ScientificDisclaimer.tsx
│   │   │   ├── charts/
│   │   │   │   ├── ProbaBarChart.tsx
│   │   │   │   ├── IAELineChart.tsx
│   │   │   │   ├── InSARTimeSeries.tsx
│   │   │   │   ├── MaintenanceGantt.tsx
│   │   │   │   └── ScenarioComparison.tsx
│   │   │   └── map/
│   │   │       ├── MapView.tsx
│   │   │       ├── StructureMarker.tsx
│   │   │       ├── RiskHeatmap.tsx
│   │   │       └── LayerControls.tsx
│   │   ├── pages/
│   │   │   ├── Cockpit.tsx
│   │   │   ├── Portfolio.tsx
│   │   │   ├── MapPage.tsx
│   │   │   ├── Inspection.tsx
│   │   │   ├── Environment.tsx
│   │   │   ├── ProbabilisticModel.tsx
│   │   │   ├── InSAR.tsx
│   │   │   ├── Maintenance.tsx
│   │   │   └── Exports.tsx
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── useAssets.ts
│   │   │   ├── useAlerts.ts
│   │   │   └── useKPIs.ts
│   │   └── types/                  # TypeScript type definitions
│   │       ├── ouvrage.ts
│   │       ├── inspection.ts
│   │       ├── environment.ts
│   │       ├── insar.ts
│   │       └── maintenance.ts
│   ├── public/
│   │   └── favicon.svg
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
├── GEODIA_SentinelCare_Cahier_des_Charges.md
└── README.md
```

---

## Proposed Changes — Sprint Breakdown

### Sprint 1: Project Foundation, Database & Cockpit

**Goal:** Project scaffolding, database setup, seed data, basic cockpit UI with KPI cards and interactive map.

**Acceptance:** All 19 structures imported, visible on map, filterable by class A–D.

---

#### Backend (Sprint 1)

##### [NEW] [requirements.txt](file:///d:/Github/GEODIA/backend/requirements.txt)
Core dependencies:
```
fastapi>=0.115
uvicorn[standard]>=0.30
sqlalchemy>=2.0
psycopg2-binary>=2.9
alembic>=1.13
pydantic>=2.0
pydantic-settings>=2.0
numpy>=1.26
pandas>=2.2
geopandas>=0.14
shapely>=2.0
scikit-learn>=1.4
pulp>=2.8
reportlab>=4.1
openpyxl>=3.1
rasterio>=1.3
python-multipart>=0.0.9
```

##### [NEW] [config.py](file:///d:/Github/GEODIA/backend/app/config.py)
- `Settings` class using `pydantic-settings` with environment variable support
- Database URL: `postgresql://user:pass@localhost:5432/geodia`
- Upload directory, CORS origins, etc.

##### [NEW] [database.py](file:///d:/Github/GEODIA/backend/app/database.py)
- SQLAlchemy async engine + session factory
- `get_db()` dependency for FastAPI

##### [NEW] [models/](file:///d:/Github/GEODIA/backend/app/models/)
All 8 ORM models matching the spec schema:
- `Ouvrage` — 19 structures with GPS, class, indices
- `Pathologie` — P1–P12 reference table
- `Inspection` — field inspection records
- `Observation` — pathology observations per inspection
- `EnvTimeseries` — environmental time series
- `InsarPoint` — InSAR deformation points
- `Proba` — 19×12 probability matrix
- `Action` — maintenance actions catalog
- `Scenario` — budget optimization scenarios

##### [NEW] [schemas/ouvrage.py](file:///d:/Github/GEODIA/backend/app/schemas/ouvrage.py)
Pydantic schemas: `OuvrageBase`, `OuvrageCreate`, `OuvrageResponse`, `OuvrageGeoJSON`

##### [NEW] [routers/assets.py](file:///d:/Github/GEODIA/backend/app/routers/assets.py)
- `GET /api/assets` — list/filter all 19 structures (JSON + GeoJSON)
- `GET /api/assets/{id}` — full structure detail
- Query params: `classe`, `famille`, `search`

##### [NEW] [routers/alerts.py](file:///d:/Github/GEODIA/backend/app/routers/alerts.py)
- `GET /api/alerts` — active alerts with priority (stub returning mock data for S1)
- `GET /api/kpis` — cockpit KPI summary endpoint

##### [NEW] [core/indices.py](file:///d:/Github/GEODIA/backend/app/core/indices.py)
Implements: `compute_ipd(ICF, IVP)`, `compute_ied(I, A, C, Acc, Inc)` — the static indices available from seed data.

##### [NEW] [main.py](file:///d:/Github/GEODIA/backend/app/main.py)
FastAPI app with CORS middleware, router includes, startup event for DB init.

##### [NEW] [seed_db.py](file:///d:/Github/GEODIA/backend/scripts/seed_db.py)
Script to parse seed CSVs and populate database tables.

##### [NEW] Seed data CSVs
- `ouvrages.csv` — 19 structures with all columns from spec (realistic simulated data based on spec tables)
- `pathologies.csv` — P1–P12 reference data
- `p0_initial.csv` — 19×12 initial probability matrix

##### [NEW] Alembic setup
Initial migration creating all tables.

---

#### Frontend (Sprint 1)

##### [NEW] Vite + React project scaffold
Initialize with `npx -y create-vite@latest ./ --template react-ts`

##### [NEW] [index.css](file:///d:/Github/GEODIA/frontend/src/index.css)
Design system with CSS custom properties:
- Dark theme with industrial/engineering aesthetic
- Color palette: deep navy blues, electric teal accents, warm amber warnings, red critical alerts
- CSS variables for spacing, typography (Inter font), border-radius, shadows
- Glassmorphism card styles, gradients, micro-animations
- Responsive breakpoints

##### [NEW] [App.tsx](file:///d:/Github/GEODIA/frontend/src/App.tsx)
- React Router v6 setup with all 9 page routes
- Persistent sidebar navigation layout
- French navigation labels matching spec

##### [NEW] [Sidebar.tsx](file:///d:/Github/GEODIA/frontend/src/components/layout/Sidebar.tsx)
Vertical navigation with icons:
`Cockpit` | `Portefeuille GC` | `Carte SIG` | `Inspection Terrain` | `Environnement` | `Modèle Proba` | `InSAR` | `Maintenance & Optimisation` | `Exports`

##### [NEW] [KPICard.tsx](file:///d:/Github/GEODIA/frontend/src/components/ui/KPICard.tsx)
Glassmorphism card component with icon, value, label, trend indicator, and micro-animations.

##### [NEW] [Cockpit.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Cockpit.tsx)
- 6 KPI cards (top row): Nombre d'ouvrages, Criticité élevée, Alertes InSAR, Inspections en attente, Indice de prévention, Économie potentielle
- Quick action buttons: Export PDF, Nouveau rapport, Plan d'inspection, etc.
- Recent alerts feed
- Scientific disclaimer banner

##### [NEW] [MapPage.tsx](file:///d:/Github/GEODIA/frontend/src/pages/MapPage.tsx)
- MapLibre GL JS with OpenStreetMap satellite tiles
- Markers colored by class A/B/C/D
- Click popup: structure name, IPD, top pathology, last inspection date
- Layer toggle controls
- Risk heatmap overlay

##### [NEW] [Portfolio.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Portfolio.tsx)
- Sortable/filterable table of all 19 structures
- Class filter chips (A/B/C/D)
- Search by name/code
- Columns: code, nom, famille, classe, ICF, IVP, IPD, IED

##### [NEW] API client
- `client.ts` — base fetch wrapper with error handling
- `assets.ts` — `getAssets()`, `getAssetById(id)`, `getKPIs()`

---

### Sprint 2: Inspection Module & Structure Sheets

**Goal:** Field inspection entry, photo uploads, E0–E3 states, pathology observations, and PDF structure sheet generation.

**Acceptance:** User can submit inspection, PDF sheet generated.

---

#### Backend (Sprint 2)

##### [NEW] [schemas/inspection.py](file:///d:/Github/GEODIA/backend/app/schemas/inspection.py)
Pydantic schemas for inspection creation, observation entry, photo metadata.

##### [NEW] [routers/inspections.py](file:///d:/Github/GEODIA/backend/app/routers/inspections.py)
- `POST /api/inspections` — create inspection record
- `GET /api/inspections` — list inspections (filter by ouvrage, date range)
- `GET /api/inspections/{id}` — full inspection detail with observations
- `POST /api/inspections/{id}/observations` — add observation
- `POST /api/inspections/{id}/photos` — upload photo(s)
- `PATCH /api/inspections/{id}/validate` — mark as validated

##### [NEW] [exporters/pdf_report.py](file:///d:/Github/GEODIA/backend/app/exporters/pdf_report.py)
- Structure sheet PDF (ReportLab): data, photos, class, scores, history
- Inspection report PDF: zones, defects, E0–E3, evidence, recommendations
- Numbered + dated reports

##### [NEW] [routers/reports.py](file:///d:/Github/GEODIA/backend/app/routers/reports.py)
- `GET /api/reports/pdf/ouvrage/{id}` — structure sheet PDF
- `GET /api/reports/pdf/inspection/{id}` — inspection report PDF

---

#### Frontend (Sprint 2)

##### [NEW] [Inspection.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Inspection.tsx)
- Inspection form: select ouvrage, date, inspecteur name, E0–E3 état selector
- Observation sub-form: pathology dropdown (P1–P12), zone, gravité (0–3), étendue (%), evidence
- Photo upload with preview
- Validation toggle
- Past inspections list with status badges

##### [NEW] [StructureSheet.tsx](file:///d:/Github/GEODIA/frontend/src/pages/StructureSheet.tsx)
- Full detail view for a single structure
- Tabs: Données, Inspections, Pathologies, Historique
- Download buttons for PDF/Excel

##### [NEW] [DataTable.tsx](file:///d:/Github/GEODIA/frontend/src/components/ui/DataTable.tsx)
Reusable sortable/filterable data table component.

##### [NEW] [StatusBadge.tsx](file:///d:/Github/GEODIA/frontend/src/components/ui/StatusBadge.tsx)
Badge component for E0–E3 states, classe A–D, urgency levels.

---

### Sprint 3: P1–P12 Probabilistic Model

**Goal:** Logistic probability model, 19×12 matrix computation, alert rules, and probability visualization.

**Acceptance:** P(p|i) matches P0 initial baseline; probability bar charts per structure.

---

#### Backend (Sprint 3)

##### [NEW] [core/model_proba.py](file:///d:/Github/GEODIA/backend/app/core/model_proba.py)
- `compute_proba(E, F, H, V, D, IAE, IAD)` — logistic formula from spec
- `classify_probability(p)` — Low/Moderate/High/Very High
- `update_proba(ouvrage_id, pathologie, new_evidence)` — recompute and log delta
- Batch computation for full 19×12 matrix

##### [NEW] [core/alerts.py](file:///d:/Github/GEODIA/backend/app/core/alerts.py)
Full alert rule engine from spec:
- Class A + P2 > 60% → critical corrosion inspection
- IAD > 0.60 + consensus ≥ 2 → GPR/leveling
- IAE > 0.70 + P8/P9 > 60% → chemical sampling
- E3 état → emergency alert
- Budget overflow → optimization trigger

##### [NEW] [schemas/proba.py](file:///d:/Github/GEODIA/backend/app/schemas/proba.py)
Probability matrix schemas, update request/response.

##### [NEW] [routers/compute.py](file:///d:/Github/GEODIA/backend/app/routers/compute.py)
- `POST /api/compute/proba` — recompute P1–P12 for one or all structures
- `GET /api/proba/{ouvrage_id}` — current probability vector
- `GET /api/proba/matrix` — full 19×12 matrix

##### [MODIFY] [routers/alerts.py](file:///d:/Github/GEODIA/backend/app/routers/alerts.py)
Replace mock data with real alert engine evaluation.

---

#### Frontend (Sprint 3)

##### [NEW] [ProbabilisticModel.tsx](file:///d:/Github/GEODIA/frontend/src/pages/ProbabilisticModel.tsx)
- Structure selector dropdown
- P1–P12 bar chart (Recharts) with probability classes color-coded
- Full 19×12 matrix heatmap view
- Probability update log with before/after delta
- Explainability panel: contributing variables, last data freshness, triggered rules, missing evidence
- Scientific disclaimer

##### [NEW] [ProbaBarChart.tsx](file:///d:/Github/GEODIA/frontend/src/components/charts/ProbaBarChart.tsx)
Grouped/stacked bar chart: P1–P12 probabilities per structure with color thresholds.

##### [NEW] [AlertCard.tsx](file:///d:/Github/GEODIA/frontend/src/components/ui/AlertCard.tsx)
Alert card with severity levels: emergency (red), critical (orange), high (amber), warning (yellow).

##### [MODIFY] [Cockpit.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Cockpit.tsx)
Connect KPI cards to live alert engine data. Add alerts feed section.

---

### Sprint 4: Environmental Layer (IAE)

**Goal:** Import environmental data (simulated), compute IAE per structure, environmental charts.

**Acceptance:** IAE charts rendered per structure; environment table visible.

---

#### Backend (Sprint 4)

##### [NEW] [importers/nasa_power.py](file:///d:/Github/GEODIA/backend/app/importers/nasa_power.py)
NASA POWER API client — temperature, humidity, rain, wind, radiation. Built ready for real API (free, no key) but loading simulated CSV for now.

##### [NEW] [importers/era5.py](file:///d:/Github/GEODIA/backend/app/importers/era5.py)
ERA5 CDS client stub — structure ready for CDS API integration.

##### [NEW] [importers/cams.py](file:///d:/Github/GEODIA/backend/app/importers/cams.py)
CAMS pollution data client stub — SO2, NO2, aerosols.

##### [NEW] [importers/sentinel2.py](file:///d:/Github/GEODIA/backend/app/importers/sentinel2.py)
Sentinel-2 NDWI client stub — water index computation.

##### [NEW] [core/indices.py](file:///d:/Github/GEODIA/backend/app/core/indices.py) (extend)
Add `compute_iae(T, H, M, R, P, W)` — full IAE formula with sub-score normalization.

##### [NEW] [routers/imports.py](file:///d:/Github/GEODIA/backend/app/routers/imports.py)
- `POST /api/import/env` — import environmental CSV or trigger API pull
- `GET /api/environment/{ouvrage_id}` — time series data
- `GET /api/environment/summary` — IAE summary table

##### [NEW] [schemas/environment.py](file:///d:/Github/GEODIA/backend/app/schemas/environment.py)
Env import schemas, time series response, IAE summary.

##### [NEW] [generate_simulated.py](file:///d:/Github/GEODIA/backend/scripts/generate_simulated.py)
Generate realistic simulated environmental time series for all 19 structures (2 years of data), flagged `is_simulated=True`.

---

#### Frontend (Sprint 4)

##### [NEW] [Environment.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Environment.tsx)
- Structure selector
- IAE score display with sub-component breakdown (T, H, M, R, P, W)
- Environmental aggressiveness table by zone: Chlorures, Sulfates, Humidité, Exposition marine, Indice Agg
- Time series line charts for each variable
- Data freshness indicator (fresh/stale/simulated)
- CSV import upload

##### [NEW] [IAELineChart.tsx](file:///d:/Github/GEODIA/frontend/src/components/charts/IAELineChart.tsx)
Multi-line chart: temperature, humidity, pollution, wind over time with IAE composite overlay.

---

### Sprint 5: InSAR Pipeline (IAD)

**Goal:** InSAR data import, descriptor computation, anomaly detection (thresholds, DBSCAN, Isolation Forest, consensus), map visualization.

**Acceptance:** Clusters visible on map; consensus classification works.

---

#### Backend (Sprint 5)

##### [NEW] [core/insar_pipeline.py](file:///d:/Github/GEODIA/backend/app/core/insar_pipeline.py)
Full pipeline from spec:
1. **Descriptor computation**: vitesse_los, cumul, acceleration, trend_change, residual_std, max_drop, r2_linear
2. **Threshold detection**: expert thresholds (-5 mm/yr, -10 mm cumul)
3. **DBSCAN spatial clustering**: eps=50m, min_samples=3
4. **Isolation Forest**: contamination=0.1, multivariate anomaly scores
5. **Consensus voting**: strong (3/3), medium (2/3), weak (1/3)

##### [NEW] [core/indices.py](file:///d:/Github/GEODIA/backend/app/core/indices.py) (extend)
Add `compute_iad(V, D, A, C, Q)` — full IAD formula.

##### [NEW] [importers/insar_csv.py](file:///d:/Github/GEODIA/backend/app/importers/insar_csv.py)
CSV/LiCSBAS format importer for InSAR point data.

##### [NEW] [schemas/insar.py](file:///d:/Github/GEODIA/backend/app/schemas/insar.py)
InSAR import schemas, point response with descriptors and consensus.

##### [MODIFY] [routers/imports.py](file:///d:/Github/GEODIA/backend/app/routers/imports.py)
Add `POST /api/import/insar` — import InSAR CSV and trigger pipeline.

##### [NEW] [routers/insar.py](file:///d:/Github/GEODIA/backend/app/routers/insar.py)
- `GET /api/insar/{ouvrage_id}` — InSAR points with descriptors
- `GET /api/insar/clusters` — spatial clusters
- `GET /api/insar/anomalies` — flagged anomalies with consensus level
- `POST /api/insar/recompute` — re-run pipeline

##### [MODIFY] [generate_simulated.py](file:///d:/Github/GEODIA/backend/scripts/generate_simulated.py)
Add simulated InSAR point data generation (with some deliberate anomalies for testing).

---

#### Frontend (Sprint 5)

##### [NEW] [InSAR.tsx](file:///d:/Github/GEODIA/frontend/src/pages/InSAR.tsx)
- Structure selector
- IAD score display
- Anomaly summary: count by consensus level (strong/medium/weak)
- InSAR time series chart per point with threshold markers
- Cluster map (points colored by cluster, anomaly intensity)
- Consensus explainability panel
- CSV import upload

##### [NEW] [InSARTimeSeries.tsx](file:///d:/Github/GEODIA/frontend/src/components/charts/InSARTimeSeries.tsx)
Line chart: LOS displacement over time with threshold markers, alert zones.

##### [MODIFY] [MapPage.tsx](file:///d:/Github/GEODIA/frontend/src/pages/MapPage.tsx)
Add InSAR layer toggle: anomaly points with consensus color coding.

##### [MODIFY] [Cockpit.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Cockpit.tsx)
Wire up InSAR alert KPI card to real pipeline data.

---

### Sprint 6: Maintenance, Optimization & Exports

**Goal:** Maintenance plan generation, PuLP budget optimization (3 scenarios), full PDF/Excel exports, final polish.

**Acceptance:** Full demo with 5-year plan, 3 scenarios, all exports working.

---

#### Backend (Sprint 6)

##### [NEW] [core/optimizer.py](file:///d:/Github/GEODIA/backend/app/core/optimizer.py)
PuLP budget optimization from spec:
- Binary selection of maintenance actions
- Maximize risk reduction under budget constraint
- S1 (économique): pure optimization
- S2 (équilibré): force all class A critical actions
- S3 (sécurité max): no compromise on high-gain actions
- Returns: selected actions, total cost, risk gain, status

##### [MODIFY] [core/indices.py](file:///d:/Github/GEODIA/backend/app/core/indices.py)
Add `compute_ipm(IPD_n, E_n, P0_n, IAE, IAD)` — full IPM formula.

##### [NEW] [schemas/maintenance.py](file:///d:/Github/GEODIA/backend/app/schemas/maintenance.py)
Maintenance plan schemas, scenario request/response.

##### [NEW] [schemas/scenario.py](file:///d:/Github/GEODIA/backend/app/schemas/scenario.py)
Scenario comparison schemas.

##### [NEW] [routers/maintenance.py](file:///d:/Github/GEODIA/backend/app/routers/maintenance.py)
- `GET /api/maintenance/plan` — 5-year maintenance plan by horizon
- `GET /api/maintenance/actions` — action catalog
- `POST /api/maintenance/actions` — add/modify actions

##### [MODIFY] [routers/compute.py](file:///d:/Github/GEODIA/backend/app/routers/compute.py)
Add `POST /api/compute/optimize` — run budget optimization for given scenario.

##### [NEW] [exporters/excel_export.py](file:///d:/Github/GEODIA/backend/app/exporters/excel_export.py)
Excel exports (openpyxl):
- Maintenance plan workbook (actions by horizon)
- Structure data sheet
- Probability matrix sheet

##### [MODIFY] [exporters/pdf_report.py](file:///d:/Github/GEODIA/backend/app/exporters/pdf_report.py)
Add:
- Risk map PDF export (with embedded map image)
- Scenario comparison report
- Dossier de consultation (ZIP with all documents)

##### [MODIFY] [routers/reports.py](file:///d:/Github/GEODIA/backend/app/routers/reports.py)
Add:
- `GET /api/reports/excel/ouvrage/{id}` — structure data Excel
- `GET /api/reports/excel/maintenance` — maintenance plan Excel
- `GET /api/reports/pdf/scenario/{id}` — scenario comparison PDF
- `GET /api/reports/pdf/risk-map` — risk map PDF
- `GET /api/reports/zip/dossier/{id}` — consultation dossier ZIP

---

#### Frontend (Sprint 6)

##### [NEW] [Maintenance.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Maintenance.tsx)
- Maintenance plan table by horizon: 0–3m / 3–6m / 6–12m / >12m
- Gantt/timeline visualization
- Budget input + scenario selector (S1/S2/S3)
- Optimization results: selected vs. deferred actions
- Scenario comparison: side-by-side risk/cost/actions
- Action detail cards with explainability

##### [NEW] [MaintenanceGantt.tsx](file:///d:/Github/GEODIA/frontend/src/components/charts/MaintenanceGantt.tsx)
Timeline/Gantt chart: actions plotted by horizon with color-coding by urgency.

##### [NEW] [ScenarioComparison.tsx](file:///d:/Github/GEODIA/frontend/src/components/charts/ScenarioComparison.tsx)
Radar or bar chart comparing S1/S2/S3 on: cost, risk reduction, coverage, class A compliance.

##### [NEW] [Exports.tsx](file:///d:/Github/GEODIA/frontend/src/pages/Exports.tsx)
- Export center: all available exports with download buttons
- Export history with numbered reports
- Filter by type: PDF, Excel, ZIP
- Preview modal for PDF documents

##### [NEW] [ScientificDisclaimer.tsx](file:///d:/Github/GEODIA/frontend/src/components/ui/ScientificDisclaimer.tsx)
Persistent banner component displaying the 4 scientific limitations from spec §21.

##### Final polish
- Responsive design validation
- Micro-animations and transitions
- Loading states and error handling
- `SIMULÉ` badges throughout UI where simulated data is displayed
- Consistent French terminology

---

## Verification Plan

### Automated Tests

```bash
# Backend unit tests
cd backend && python -m pytest tests/ -v

# Core logic tests
python -m pytest tests/test_indices.py     # ICF, IVP, IPD, IED, IAE, IAD, IPM
python -m pytest tests/test_proba.py       # Logistic model P1–P12 vs spec values
python -m pytest tests/test_insar.py       # Descriptors, DBSCAN, IsoForest, consensus
python -m pytest tests/test_optimizer.py   # PuLP optimization S1/S2/S3

# API integration tests
python -m pytest tests/test_api.py -v

# Frontend build check
cd frontend && npm run build
```

### Manual Verification (per Acceptance Criteria §20)

| # | Criterion | Sprint | How to verify |
|---|---|---|---|
| 1 | 19 structures on map, filterable by class | S1 | Open map page, toggle class filters |
| 2 | Structure sheets with IPD, IED, P1–P12, history | S2–S3 | Click structure → verify all tabs |
| 3 | Field inspection with photos and E0–E3 | S2 | Submit inspection form → verify DB |
| 4 | Env + InSAR layers imported and timestamped | S4–S5 | Import CSV → verify time series charts |
| 5 | System computes IAE, IAD, P(p|i), IPM with explanations | S3–S5 | Trigger recompute → verify outputs |
| 6 | InSAR pipeline: threshold, DBSCAN, IsoForest, consensus | S5 | Import InSAR data → verify clusters on map |
| 7 | Maintenance plan by horizon and budget | S6 | Open maintenance page → verify timeline |
| 8 | 3 optimization scenarios (S1/S2/S3) | S6 | Run optimization → compare scenarios |
| 9 | PDF/Excel exports readable and numbered | S2+S6 | Download exports → verify content |
| 10 | No auto-decision without field evidence | All | Check disclaimer + explainability panels |
| 11 | Simulated data flagged `SIMULÉ` | All | Check badges on all pages using sim data |

---

## Timeline Estimate

| Sprint | Focus | Estimated Duration |
|---|---|---|
| S1 | Foundation, DB, Cockpit, Map, Portfolio | ~3–4 days |
| S2 | Inspection module, Structure sheets, PDF | ~2–3 days |
| S3 | P1–P12 model, Alert engine, Probability UI | ~2–3 days |
| S4 | Environmental IAE, Importers, Charts | ~2–3 days |
| S5 | InSAR IAD pipeline, Anomaly detection, Map layers | ~3–4 days |
| S6 | Maintenance, Optimization, Exports, Polish | ~3–4 days |
| **Total** | | **~15–21 days** |
