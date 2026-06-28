# GÉODIA / SentinelCare GC — Technical Specification
**Client:** OCP — Pôle Industriel de Jorf Lasfar, Service Génie Civil
**Scope:** 19 reinforced concrete structures in marine/chemical environments
**Goal:** AI-assisted preventive maintenance, inspection, and budget optimization platform

---

## 1. Project Overview

Build a local/web decision-support platform that:
- Centralizes asset data for 19 GC structures (classes A–D)
- Computes priority indices (ICF, IVP, IPD, IED, IPM)
- Integrates environmental aggressiveness (IAE) and InSAR deformation layers (IAD)
- Estimates pathology probabilities P1–P12 per structure using a logistic model
- Generates preventive maintenance plans and budget-constrained optimization scenarios
- Exports full inspection dossiers as PDF/Excel

**Design philosophy:** The system does not replace the structural engineer. It prioritizes, documents, and makes decisions traceable.

---

## 2. Recommended Tech Stack

### Option A — Rapid Prototype (recommended for V1)
| Layer | Technology |
|---|---|
| Frontend | **Streamlit** (Python, zero-build UI, fast iteration) |
| Maps | **Folium** + **Leaflet.js** embedded in Streamlit |
| Charts | **Plotly** |
| Backend logic | **Python** (single-process for prototype) |
| Database | **SQLite** via **SQLAlchemy** ORM |
| AI/ML | **scikit-learn** (DBSCAN, Isolation Forest), **NumPy**, **Pandas** |
| Optimization | **PuLP** (linear programming for budget scenarios) |
| Geospatial | **GeoPandas**, **Shapely**, **Rasterio** |
| PDF exports | **ReportLab** or **WeasyPrint** |
| Excel exports | **openpyxl** |

### Option B — Production-Grade
| Layer | Technology |
|---|---|
| Frontend | **React 18** + **TypeScript** + **Tailwind CSS** |
| Maps | **MapLibre GL JS** |
| Charts | **Recharts** or **Visx** |
| Backend | **FastAPI** (Python) + **Celery** (async tasks) |
| Database | **PostgreSQL** + **PostGIS** extension |
| Containerization | **Docker** + **docker-compose** |
| AI/ML | same as Option A |

> **Recommendation:** Start with Option A. Migrate to Option B when prototype is validated.

---

## 3. Repository Structure

```
geodia-sentinelcare/
├── app/
│   ├── main.py                  # Streamlit entrypoint
│   ├── pages/
│   │   ├── 01_cockpit.py
│   │   ├── 02_portfolio.py
│   │   ├── 03_map.py
│   │   ├── 04_inspection.py
│   │   ├── 05_environment.py
│   │   ├── 06_probabilistic_model.py
│   │   ├── 07_insar.py
│   │   ├── 08_maintenance.py
│   │   └── 09_exports.py
│   ├── components/              # Reusable UI components
│   ├── core/
│   │   ├── indices.py           # ICF, IVP, IPD, IED, IAE, IAD, IPM formulas
│   │   ├── model_proba.py       # Logistic model P1–P12
│   │   ├── insar_pipeline.py    # Descriptors, DBSCAN, IsoForest, consensus
│   │   ├── optimizer.py         # PuLP budget optimization
│   │   └── alerts.py            # Alert rule engine
│   ├── data/
│   │   ├── importers/
│   │   │   ├── nasa_power.py    # NASA POWER API
│   │   │   ├── era5.py          # Copernicus ERA5
│   │   │   ├── cams.py          # CAMS pollution
│   │   │   ├── sentinel2.py     # NDWI water index
│   │   │   └── insar_csv.py     # LiCSBAS/CSV import
│   │   └── exporters/
│   │       ├── pdf_report.py
│   │       └── excel_export.py
│   └── db/
│       ├── models.py            # SQLAlchemy ORM models
│       ├── session.py
│       └── migrations/
├── data/
│   ├── seed/
│   │   ├── ouvrages.csv         # 19 structures with GPS, class, indices
│   │   ├── pathologies.csv      # P1–P12 reference data
│   │   ├── p0_initial.csv       # 19x12 initial probability matrix
│   │   ├── actions_maintenance.csv
│   │   └── inspections_template.csv
│   └── simulated/              # Clearly flagged as SIMULATED in DB
│       ├── env_timeseries_sim.csv
│       └── insar_points_sim.csv
├── tests/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 4. Database Schema (SQLite / PostgreSQL)

### `ouvrages` — Asset master table
```sql
CREATE TABLE ouvrages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT NOT NULL UNIQUE,          -- e.g. "R-102"
    nom         TEXT NOT NULL,
    famille     TEXT NOT NULL,                 -- hydraulique, réservoir, bâtiment, fosse, canal, station
    lat         REAL NOT NULL,
    lon         REAL NOT NULL,
    classe      TEXT NOT NULL CHECK(classe IN ('A','B','C','D')),
    icf         REAL,                          -- Criticité fonctionnelle
    ivp         REAL,                          -- Vulnérabilité potentielle
    ipd         REAL,                          -- Priorité diagnostic = 0.70*ICF + 0.30*IVP
    ied         REAL,                          -- Effort diagnostique
    exposition  TEXT,                          -- XS3, XA3, HY3, ST2 ...
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `pathologies` — Reference P1–P12
```sql
CREATE TABLE pathologies (
    code        TEXT PRIMARY KEY,              -- P1 .. P12
    famille     TEXT,
    description TEXT,
    symptomes   TEXT,
    methodes    TEXT,                          -- CND methods
    mecanismes  TEXT
);
```

### `inspections` — Field inspection records
```sql
CREATE TABLE inspections (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ouvrage_id  INTEGER REFERENCES ouvrages(id),
    date        DATE NOT NULL,
    inspecteur  TEXT NOT NULL,
    etat        TEXT CHECK(etat IN ('E0','E1','E2','E3')),
    photos      TEXT,                          -- JSON array of file paths
    commentaire TEXT,
    validation  BOOLEAN DEFAULT FALSE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `observations` — Pathology observations per inspection
```sql
CREATE TABLE observations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    inspection_id INTEGER REFERENCES inspections(id),
    pathologie    TEXT REFERENCES pathologies(code),
    zone          TEXT,
    gravite       INTEGER CHECK(gravite BETWEEN 0 AND 3),
    etendue       REAL,                        -- % surface affected
    preuve        TEXT,                        -- evidence description
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `env_timeseries` — Environmental time series
```sql
CREATE TABLE env_timeseries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ouvrage_id    INTEGER REFERENCES ouvrages(id),
    date          DATETIME NOT NULL,
    temperature   REAL,
    humidite      REAL,
    pluie         REAL,
    vent          REAL,
    pollution_so2 REAL,
    pollution_no2 REAL,
    ndwi          REAL,                        -- water index
    iae           REAL,                        -- computed IAE
    source        TEXT,
    fraicheur     TEXT,                        -- "fresh"/"stale"/"simulated"
    is_simulated  BOOLEAN DEFAULT FALSE
);
```

### `insar_points` — InSAR deformation points
```sql
CREATE TABLE insar_points (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ouvrage_id  INTEGER REFERENCES ouvrages(id),
    lat         REAL,
    lon         REAL,
    date_start  DATE,
    date_end    DATE,
    vitesse_los REAL,                          -- mm/year
    cumul       REAL,                          -- mm total
    acceleration REAL,
    r2          REAL,
    cluster_id  INTEGER,
    iad         REAL,                          -- computed IAD
    source      TEXT,
    is_simulated BOOLEAN DEFAULT FALSE
);
```

### `proba` — Probability matrix 19×12
```sql
CREATE TABLE proba (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ouvrage_id   INTEGER REFERENCES ouvrages(id),
    pathologie   TEXT REFERENCES pathologies(code),
    p0           REAL,                         -- initial prior %
    p_current    REAL,                         -- updated probability %
    iae          REAL,
    iad          REAL,
    source       TEXT,
    computed_by  TEXT,
    computed_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `actions` — Maintenance action catalog
```sql
CREATE TABLE actions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ouvrage_id    INTEGER REFERENCES ouvrages(id),
    pathologie    TEXT,
    type_action   TEXT,                        -- inspection, nettoyage, réparation...
    cout          REAL,                        -- DH
    duree_jours   INTEGER,
    urgence       TEXT CHECK(urgence IN ('0-3m','3-6m','6-12m','>12m')),
    statut        TEXT DEFAULT 'planifié',
    declencheur   TEXT,                        -- trigger condition
    dependances   TEXT,                        -- JSON array of action IDs
    preuve_min    TEXT
);
```

### `scenarios` — Budget optimization scenarios
```sql
CREATE TABLE scenarios (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nom             TEXT,                      -- S1/S2/S3
    budget          REAL,
    actions_retenues TEXT,                     -- JSON array of action IDs
    risque_initial  REAL,
    risque_final    REAL,
    gain_risque     REAL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 5. Core Computed Indices

### 5.1 Environmental Aggressiveness Index (IAE)
```python
def compute_iae(T, H, M, R, P, W) -> float:
    """
    T = temperature score (heat, amplitude, hot days)
    H = humidity score (wet-dry cycles, humectation duration)
    M = marine exposure score (distance to sea + wind direction + marine wind hours)
    R = rain score (rainfall, runoff, stagnation)
    P = pollution score (SO2, NO2, aerosols, dust)
    W = wind score (speed, direction, chemical transport)
    All inputs normalized 0-1.
    """
    return 0.20*T + 0.20*H + 0.20*M + 0.15*R + 0.15*P + 0.10*W
```

### 5.2 Deformation Anomaly Index (IAD)
```python
def compute_iad(V, D, A, C, Q) -> float:
    """
    V = LOS velocity score
    D = cumulative displacement score
    A = acceleration score
    C = trend change score
    Q = residual std score (signal regularity)
    All inputs normalized 0-1.
    """
    return 0.30*V + 0.25*D + 0.20*A + 0.15*C + 0.10*Q
```

### 5.3 Maintenance Priority Index (IPM)
```python
def compute_ipm(IPD_n, E_n, P0_n, IAE, IAD) -> float:
    """
    IPD_n = normalized IPD score
    E_n   = normalized inspection state
    P0_n  = normalized max pathology probability
    """
    return 0.30*IPD_n + 0.20*E_n + 0.20*P0_n + 0.15*IAE + 0.15*IAD
```

### 5.4 Diagnostic Priority (IPD)
```python
def compute_ipd(ICF, IVP) -> float:
    return 0.70 * ICF + 0.30 * IVP
    # Class A if IPD >= 90%
```

### 5.5 Diagnostic Effort (IED)
```python
def compute_ied(I, A, C, Acc, Inc) -> float:
    """
    I   = inspection complexity
    A   = aggressiveness
    C   = criticality
    Acc = accessibility
    Inc = uncertainty
    """
    return 100 * (0.35*I + 0.25*A + 0.20*C + 0.10*Acc + 0.10*Inc)
```

---

## 6. Probabilistic Model P1–P12

### Logistic Formula
```python
import numpy as np

def compute_proba(E, F, H, V, D, IAE, IAD) -> float:
    """
    E   = exposure-pathology compatibility (XS3, XA3, HY3, ST2) — from report + geolocation
    F   = structure family compatibility (canal, basin, building, pit, station)
    H   = anomaly/intervention history compatibility
    V   = visible indices (crack, spalling, corrosion, deposit, leak, erosion) — field inspection
    D   = contradictory evidence (reliable measure reducing plausibility) — CND/lab
    IAE = environmental aggressiveness index (dynamic)
    IAD = deformation anomaly index (InSAR)
    """
    z = -2.2 + 1.4*E + 1.2*F + 1.1*H + 1.5*V - 1.3*D + 1.0*IAE + 0.9*IAD
    return 1 / (1 + np.exp(-z))
```

### Probability Classes
| Range | Level | Recommended Decision |
|---|---|---|
| < 25% | Low | Baseline observation, no specific testing |
| 25–49% | Moderate | Conditional test if visible zone or class A/B structure |
| 50–74% | High | Targeted verification, CND or lab per P1–P12 |
| ≥ 75% | Very High | Close inspection + immediate confirmation |

### Update Rule
After each new field evidence, recompute `P(p|i)` and log: `{date, ouvrage_id, pathologie, old_p, new_p, source, user}`.

---

## 7. P1–P12 Reference Pathologies

| Code | Mechanism | Confirmation Methods |
|---|---|---|
| P1 | Insufficient cover | Pachymeter |
| P2 | Chloride-induced corrosion | Potential, resistivity, chloride content |
| P3 | Submerged corrosion | Potential, chlorides |
| P4 | Service cracking | Crack mapping, UPV |
| P5 | Structural cracking / low concrete quality | UPV, Schmidt hammer, core samples |
| P6 | Scour / sub-slab cavity | GPR, bathymetry, InSAR |
| P7 | Carbonation | Phenolphthalein, potential |
| P8 | Phosphate attack | pH, phosphates, XRD |
| P9 | Sulfate / phosphogypsum attack | pH, sulfates, XRD |
| P10 | Joint / waterstop defects | Visual, endoscopy |
| P11 | Abrasion / hydraulic erosion | Visual, geometric inspection |
| P12 | Settlement / heave | InSAR, leveling, geometric inspection |

---

## 8. InSAR Pipeline

### Descriptors to Compute per Point
```python
insar_descriptors = {
    "vitesse_los":   "linear slope mm/year (subsidence or uplift)",
    "cumul":         "total displacement mm over period",
    "acceleration":  "rate change — worsening movement",
    "trend_change":  "rupture between first/second half of series",
    "residual_std":  "signal regularity around trend",
    "max_drop":      "largest single-step negative jump",
    "r2_linear":     "linear trend reliability"
}

# Alert thresholds
ALERTS = {
    "vitesse_los": -5,    # mm/year
    "cumul":       -10,   # mm
}
```

### Detection Pipeline
```python
# Step 1 — Expert thresholding
def threshold_detection(df) -> pd.Series:
    """Returns binary label 0/1 with reason string."""

# Step 2 — DBSCAN spatial clustering
from sklearn.cluster import DBSCAN
def dbscan_detection(coords, eps=50, min_samples=3) -> np.ndarray:
    """Returns cluster IDs; -1 = noise/isolated."""

# Step 3 — Isolation Forest multivariate anomaly
from sklearn.ensemble import IsolationForest
def isolation_forest_detection(features_df, contamination=0.1) -> np.ndarray:
    """Returns anomaly scores 0–1."""

# Step 4 — Consensus vote
def consensus(threshold_label, dbscan_label, isoforest_score, threshold=0.5):
    """
    Returns: confidence = 'strong' (3/3), 'medium' (2/3), 'weak' (1/3)
    Priority max if 3/3 agreement.
    """
```

---

## 9. Alert Rule Engine

```python
ALERT_RULES = [
    {
        "condition": lambda o: o.classe == 'A' and o.proba['P2'] > 0.60,
        "action": "Inspection corrosion obligatoire",
        "severity": "critical"
    },
    {
        "condition": lambda o: o.iad > 0.60 and o.insar_consensus >= 2,
        "action": "GPR / nivellement / inspection radier",
        "severity": "high"
    },
    {
        "condition": lambda o: o.iae > 0.70 and (o.proba['P8'] > 0.60 or o.proba['P9'] > 0.60),
        "action": "Prélèvements pH, sulfates, phosphates",
        "severity": "high"
    },
    {
        "condition": lambda o: o.etat_terrain == 'E3',
        "action": "Alerte immédiate + sécurisation",
        "severity": "emergency"
    },
    {
        "condition": lambda o: o.total_action_cost > o.budget,
        "action": "Lancer optimisation scénarios",
        "severity": "warning"
    }
]
```

---

## 10. Budget Optimization (PuLP)

```python
from pulp import *

def optimize_budget(actions: list[dict], budget: float, scenario: str) -> dict:
    """
    actions: [{id, ouvrage_id, cout, gain_risque, urgence, classe}]
    scenario: 'S1' (économique) | 'S2' (équilibré) | 'S3' (sécurité max)
    """
    prob = LpProblem("maintenance_optimization", LpMaximize)
    x = {a['id']: LpVariable(f"x_{a['id']}", cat='Binary') for a in actions}

    # Objective: maximize risk reduction
    prob += lpSum(a['gain_risque'] * x[a['id']] for a in actions)

    # Budget constraint
    prob += lpSum(a['cout'] * x[a['id']] for a in actions) <= budget

    # Scenario-specific constraints
    if scenario == 'S2':
        # Force all class A critical actions
        for a in actions:
            if a['classe'] == 'A' and a['urgence'] == '0-3m':
                prob += x[a['id']] == 1
    elif scenario == 'S3':
        # No compromise on high-priority
        for a in actions:
            if a['gain_risque'] > 0.8:
                prob += x[a['id']] == 1

    prob.solve(PULP_CBC_CMD(msg=0))
    return {
        "selected": [a['id'] for a in actions if value(x[a['id']]) == 1],
        "total_cost": sum(a['cout'] for a in actions if value(x[a['id']]) == 1),
        "risk_gain": sum(a['gain_risque'] for a in actions if value(x[a['id']]) == 1),
        "status": LpStatus[prob.status]
    }
```

---

## 11. API Endpoints (FastAPI — Option B)

```
GET  /assets                    → List/filter all 19 structures (JSON + GeoJSON)
GET  /asset/{id}                → Full structure sheet (JSON)
POST /inspection                → Add field inspection record
POST /import/env                → Import weather/climate CSV or API pull
POST /import/insar              → Import InSAR series or LiCSBAS points
POST /compute/proba             → Recompute P1–P12 matrix
POST /compute/optimize          → Budget optimization → scenario
GET  /report/pdf/{id}           → Export structure sheet or full report (PDF)
GET  /report/excel/{id}         → Export maintenance plan (Excel)
GET  /maintenance/plan          → 5-year maintenance plan
GET  /alerts                    → Active alerts with priority
```

---

## 12. UI Modules

### Navigation (vertical menu)
`Cockpit` | `Portefeuille GC` | `Carte SIG` | `Inspection Terrain` | `Environnement` | `Modèle Proba` | `InSAR` | `Maintenance & Optimisation` | `Exports` | `Paramètres`

### Cockpit — KPI Cards (top row)
| KPI | Description |
|---|---|
| Nombre d'ouvrages | Total portfolio count |
| Criticité élevée | Count with IPD class A |
| Alertes InSAR | Active InSAR anomalies |
| Inspections en attente | Overdue inspections |
| Indice de prévention | Global prevention score /100 |
| Économie potentielle | Budget savings vs no-action scenario |

### Carte SIG
- Satellite basemap (OpenStreetMap or ESRI tiles)
- Markers colored by class A/B/C/D
- Risk heatmap with legend: 0–20 / 20–40 / 40–60 / 60–80 / 80–100
- Popup on click: structure name, IPD, top pathology probability, last inspection date, link to sheet
- Toggle layers: structures, InSAR anomalies, water zones, environmental aggressiveness

### Charts Required
- Bar chart: P1–P12 probability per structure (grouped or stacked)
- Table: environmental aggressiveness by zone (Chlorures, Sulfates, Humidité, Exposition marine, Indice Agg)
- Gantt/timeline: maintenance horizon 0–3m / 3–6m / 6–12m / >12m
- Line chart: InSAR time series per point with threshold markers

### Quick Actions Buttons
- Export PDF unique
- Nouveau rapport
- Plan d'inspection
- Ajouter alerte
- Demande d'intervention

---

## 13. Data Sources & External APIs

| Source | Data | Frequency | Notes |
|---|---|---|---|
| NASA POWER Hourly API | Temperature, humidity, rain, wind, radiation | Hourly/daily | Free, no key required |
| Copernicus ERA5 (CDS) | Reanalysis climate | Hourly | Requires CDS account |
| Copernicus CAMS | SO2, NO2, aerosols, dust | Daily | Requires CDS account |
| Sentinel-2 (CDSE) | NDWI water index | Every 5–10 days | Requires CDSE account |
| Sentinel-1 / LiCSBAS | InSAR LOS displacement | 6–12 days | CSV import supported |

**Always store per imported record:** `source`, `date_acquisition`, `date_import`, `resolution`, `computation_method`, `unit`, `user`, `quality_status`, `is_simulated`.

---

## 14. Seed Data (Required in `/data/seed/`)

### `ouvrages.csv` — 19 structures
Columns: `code, nom, famille, lat, lon, classe, icf, ivp, ipd, ied, exposition`

Priority structures for V1:
| Rank | Structure | IPD | Class |
|---|---|---|---|
| 1 | Déversoir de l'eau de mer | 98.8 | A |
| 2 | Déversoir du canal | 98.8 | A |
| 3 | Bassin de tranquillisation REM1 | 98.2 | A |
| 4 | Canal de rejet de l'eau de mer | 94.4 | A |
| 5 | Bâtiment de la centrale électrique | 91.5 | A |
| 6 | Canal de connexion REM1/REM2 | 90.6 | A |

### `p0_initial.csv` — Initial probability matrix (extract)
| Ouvrage | P2 | P3 | P6 | P7 | P8 | P9 | P12 |
|---|---|---|---|---|---|---|---|
| Déversoir eau de mer | 66 | 50 | 49 | 30 | 21 | 19 | 39 |
| Canal rejet eau de mer | 66 | 56 | 54 | 29 | 38 | 30 | 39 |
| Bâtiment centrale électrique | 41 | 20 | 21 | 70 | 19 | 18 | 38 |
| Fosses collectrices phosphogypse | 48 | 49 | 36 | 30 | 70 | 70 | 37 |
| Bassin aspiration eau de mer | 66 | 59 | 56 | 29 | 22 | 20 | 42 |

### `actions_maintenance.csv`
Columns: `id, ouvrage_id, pathologie, type_action, cout_dh, duree_jours, urgence, declencheur, preuve_min`

### `inspections_template.csv`
Columns: `ouvrage_id, date, inspecteur, etat, zone, pathologie_observee, gravite, etendue, commentaire`

---

## 15. Budget Reference Points
- **Diagnostic campaign (1st):** 303,676 DH
- **5-year preventive maintenance reference:** 6,600,000 DH (post terrain recalibration)

---

## 16. User Roles & Permissions

| Role | Allowed | Blocked |
|---|---|---|
| Admin | Settings, imports, users, references | Nothing |
| Ingénieur GC | Technical validation, priorities, sheets, action plans | Permanent deletion |
| Inspecteur | Field entry, photos, E0–E3 state, defects | Model/calculation modification |
| Manager | Read, budget arbitration, exports | Raw technical entry |

---

## 17. Explainability Requirements

Every recommendation must display:
- Final score and contributing variables
- Last data used + freshness level
- Triggered rules
- Missing evidence
- Recommended next action

**Critical rule:** No automatic decision is presented as a confirmed diagnosis without field evidence. Always separate: `observation → hypothesis → evidence → confirmed diagnosis → decision`.

---

## 18. Export Deliverables

| Deliverable | Content | Format |
|---|---|---|
| Fiche ouvrage | Data, photos, class, scores, P1–P12, history | PDF / Excel |
| Rapport inspection | Zones, defects, E0–E3, evidence, recommendations | PDF |
| Carte risque | SIG map with active layers and legend | PNG / PDF |
| Plan maintenance | Actions 0–3m / 3–6m / 6–12m / >12m / 5-year | Excel / PDF |
| Rapport scénario | Budget, selected/deferred actions, residual risk | PDF |
| Dossier consultation | Input data for contractors + inspection requirements | ZIP / PDF |

---

## 19. Sprint Plan (6 Sprints)

| Sprint | Objective | Deliverables | Acceptance |
|---|---|---|---|
| S1 | Project base: tables, import 19 structures, cockpit UI | SQLite, home screen, map | Data visible on map |
| S2 | Inspection module and structure sheets | Forms, photos, E0–E3 states | PDF sheet generated |
| S3 | P1–P12 model + logistic probabilities | 19×12 matrix, alert rules | Matches P0 initial baseline |
| S4 | Environment IAE | NASA/ERA5/CAMS/CSV import, normalization | Charts per structure |
| S5 | InSAR IAD (MAR-inspired) | Descriptors, thresholds, DBSCAN, Isolation Forest | Clusters + map |
| S6 | Maintenance / optimization / exports | 5-year plan, 3 scenarios, final PDF | Full demo |

---

## 20. Acceptance Criteria (V1 Prototype)

1. All 19 structures imported, displayed on map, filterable by class A–D
2. Structure sheets contain IPD, IED, expositions, P1–P12 probabilities and history
3. User can enter field inspection with photos and E0–E3 state
4. Weather/environment and InSAR layers can be imported and timestamped
5. System computes IAE, IAD, P(p|i) and IPM with result explanations
6. InSAR pipeline produces threshold, DBSCAN, Isolation Forest and consensus outputs
7. Maintenance plan generated per horizon and budget
8. Optimization provides at least 3 comparable scenarios (S1/S2/S3)
9. PDF/Excel exports are readable, archived and numbered
10. No automatic decision presented as confirmed diagnosis without field evidence
11. All simulated data clearly flagged as `SIMULÉ` in the database and in reports

---

## 21. Scientific Limitations (Must Be Displayed In-App)

> ⚠️ Les probabilités ne sont pas des diagnostics.
> Les données satellites ne donnent pas la cause d'une pathologie béton.
> L'InSAR signale des déformations dans la ligne de visée, pas la cause.
> Toute action de maintenance doit être validée par un ingénieur et par des preuves terrain.

---

*Prepared for AI engineer / developer to build the GÉODIA / SentinelCare GC prototype — OCP Jorf Lasfar.*
