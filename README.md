# 🕸️ CERBERUS GRAVITY

**Risk-Weighted Attack Graph Intelligence Engine**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](.)
[![Python](https://img.shields.io/badge/python-3.12%2B-green.svg)](.)
[![Node](https://img.shields.io/badge/node-18--22-green.svg)](.)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)
[![Author](https://img.shields.io/badge/author-Sudeepa%20Wanigarathna-purple.svg)](.)

> Experimental cybersecurity research platform for studying how **asset criticality**, **privilege**, **reachability**, **trust**, and **graph structure** influence attack-path risk.

**Author:** Sudeepa Wanigarathna  
**© 2026 Sudeepa Wanigarathna**

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Research Motivation](#2-research-motivation)
3. [Threat Model & Scope](#3-threat-model--scope)
4. [Gravity Model](#4-gravity-model)
5. [Mathematical Formulation](#5-mathematical-formulation)
6. [Architecture](#6-architecture)
7. [Technology Stack](#7-technology-stack)
8. [Features](#8-features)
9. [Installation](#9-installation)
10. [Quick Start](#10-quick-start)
11. [Docker Setup](#11-docker-setup)
12. [Demo & Datasets](#12-demo--datasets)
13. [Graph Model](#13-graph-model)
14. [Gravity Algorithm](#14-gravity-algorithm)
15. [Attack Path Algorithm](#15-attack-path-algorithm)
16. [Research Mode](#16-research-mode)
17. [Experiments](#17-experiments)
18. [API Documentation](#18-api-documentation)
19. [Frontend Dashboard](#19-frontend-dashboard)
20. [Project Structure](#20-project-structure)
21. [Testing](#21-testing)
22. [Limitations](#22-limitations)
23. [Ethical Use](#23-ethical-use)
24. [Future Work](#24-future-work)
25. [Author](#25-author)
26. [License](#26-license)

---

## 1. Project Overview
 <br>
<img width="1913" height="1047" alt="g" src="https://github.com/user-attachments/assets/0a979bed-7a10-4c65-8980-9cb0d454344e" /> <br> <br>


**CERBERUS GRAVITY** is a modular research platform that constructs **risk-weighted attack graphs** and quantifies how high-value, highly privileged, and highly reachable assets pull attack paths toward them — analogous to gravitational attraction.

It is **not** a vulnerability scanner and **not** an exploitation framework.

It is designed for:

- Authorized lab environments  
- Synthetic enterprise graphs  
- Isolated cyber ranges  
- Academic and defensive research  

The centerpiece is an interactive attack graph that makes the following immediately visible:

- Where are the **gravity wells**?  
- Which assets attract the most attack paths?  
- Which paths have the greatest **strategic importance**?  
- Which assets create the largest **blast radius**?  
- Which remediation produces the greatest reduction in modelled risk?  

---

## 2. Research Motivation

Traditional risk tools often score assets in isolation. Real attack paths, however, are shaped by **relationships**: trust, privilege transitions, reachability, and business value.

CERBERUS GRAVITY formalizes the research hypothesis:

> High-value, highly privileged, highly reachable assets exert stronger influence on surrounding attack paths. That influence can be modelled, propagated, ranked, and stress-tested under what-if conditions.

All scores produced by the platform are **experimental research constructs**. They are not industry-standard risk metrics and must not be treated as such.

---

## 3. Threat Model & Scope

| In scope | Out of scope |
|----------|----------------|
| Synthetic / lab attack graphs | Live unauthorized scanning |
| Privilege & trust modelling | Automatic exploitation |
| Path ranking & blast radius | Internet-scale reconnaissance |
| Remediation *modelled* impact | Guarantees about real-world risk |
| Research parameter sweeps | Offensive tooling |

The system never invents graph data and never performs uncontrolled third-party exploitation.

---

## 4. Gravity Model

Each asset receives a **Gravity** score in the range **0–100**.

### Factors (all on 0–100 scale)

| Factor | Description |
|--------|-------------|
| **Business value** | Importance of the asset to the enterprise |
| **Privilege level** | Administrative / high-privilege potential |
| **Reachability** | How easily the asset can be reached from entry points |
| **Trust level** | Strength of trust relationships involving the asset |
| **Exposure** | External or internal attack surface exposure |
| **Criticality** (optional blend) | Operational criticality |

### Configurable weights

Researchers can change:

- `asset_value_weight`  
- `privilege_weight`  
- `reachability_weight`  
- `trust_weight`  
- `exposure_weight`  

Default values ship with the platform and can be modified in **Research Mode**.

---

## 5. Mathematical Formulation

### Asset Gravity (experimental)

Let factors \(f_i \in [0, 100]\) and weights \(w_i > 0\).

**Weighted arithmetic mean (base):**

\[
\text{base} = \frac{\sum_i w_i \cdot f_i}{\sum_i w_i}
\]

**Weighted geometric mean (interaction / compounding):**

\[
\text{interaction} = 100 \cdot \prod_i \left(\max\left(\frac{f_i}{100}, 0.01\right)\right)^{w_i / \sum w}
\]

**Combined gravity:**

\[
G = 0.65 \cdot \text{base} + 0.35 \cdot \text{interaction}
\]

Optional mild blend with criticality \(C\):

\[
G \leftarrow 0.80 \cdot G + 0.20 \cdot C
\]

Result is clamped to \([0, 100]\).

> This formula is an **experimental research model**, not a standardized risk equation.

### Gravity Propagation

Influence from a high-gravity source \(s\) to a node \(t\) at graph distance \(d\):

\[
I(s \to t) = G_s \cdot \delta^{d} \cdot \tau \cdot \rho
\]

Where:

- \(\delta\) = decay factor (default `0.6`)  
- \(\tau\) = trust / relationship factor  
- \(\rho\) = optional privilege-transition bonus  
- Maximum propagation distance is configurable  

### Path metrics

For a path \(P = (n_1, \ldots, n_k)\):

| Metric | Definition |
|--------|------------|
| Path distance | \(k - 1\) |
| Path gravity | \(\sum G(n_i)\) |
| Average gravity | path gravity / \(k\) |
| Max node gravity | \(\max G(n_i)\) |
| Risk (experimental) | weighted mix of avg gravity, max gravity, trust, privilege transitions |
| Strategic attraction | balances gravity, inverse distance, peak gravity, risk |
| Path efficiency | path gravity / distance |

### Graph-theoretic metrics (separate from gravity)

- Degree centrality  
- Betweenness centrality  
- Closeness centrality  
- PageRank  
- Eigenvector centrality  

**Strategic Criticality** combines gravity with selected centralities (weights configurable). This is also an experimental CERBERUS metric, not a standard.

### Other experimental metrics

| Metric | Intent |
|--------|--------|
| Gravity concentration | Gini-like inequality of gravity mass |
| Gravity well density | Fraction of nodes above a gravity threshold |
| Attack surface entropy | Shannon entropy of binned gravity distribution |
| Blast score | Modelled impact if a node is compromised |
| Gravity gradient | Local steepness of gravity around a node |

---

## 6. Architecture

```
                     CERBERUS GRAVITY
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Data Ingestion                API Layer
              │                           │
              ▼                           ▼
       Asset Discovery              FastAPI Backend
              │                           │
              ▼                           ▼
       Graph Construction ───────► Graph Engine (NetworkX)
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
              Gravity Engine        Path Engine          Risk Engine
                    │                     │                     │
                    └─────────────────────┼─────────────────────┘
                                          │
                                          ▼
                                  Simulation Engine
                                          │
                                          ▼
                                  Visualization API
                                          │
                                          ▼
                                   Next.js Dashboard
```

### Backend modules

| Module | Role |
|--------|------|
| `gravity/` | Gravity engine, propagation, experimental metrics |
| `graph/` | Graph construction, path analysis, criticality, blast radius |
| `services/` | Orchestration (`AnalysisService`) |
| `api/v1/` | REST endpoints |
| `models/` | SQLAlchemy entities (assets, identities, relationships, experiments) |
| `schemas/` | Pydantic request/response models |

### Frontend modules

| Area | Role |
|------|------|
| Dashboard | Stats, distribution, top assets, graph preview, paths |
| Attack Graph | Full React Flow interactive view |
| Paths | Ranked paths + highlighting |
| Blast Radius | Per-node impact analysis |
| Remediation | Before → after simulation UI |
| Research Mode | Weight controls + experiment persistence |

---

## 7. Technology Stack

### Backend

- Python 3.12+  
- FastAPI  
- Pydantic / pydantic-settings  
- NetworkX  
- NumPy / Pandas  
- SQLAlchemy / aiosqlite  
- Uvicorn  
- pytest  

### Frontend

- Next.js 14  
- TypeScript  
- React 18  
- Tailwind CSS  
- React Flow  
- Recharts  
- Lucide Icons  

### Deployment

- Docker / Docker Compose  
- Local Linux development  
- `install.sh` / `start-backend.sh` / `start-frontend.sh`  

---

## 8. Features

### Core analysis

- Asset gravity computation (configurable weights)  
- Gravity propagation across the graph  
- Multi-mode attack path ranking  
- Gravity well detection (single- and multi-node)  
- Strategic criticality scores  
- Blast radius analysis  
- Remediation impact simulation  
- What-if change application  

### Research

- Live coefficient editing  
- Experiment save / list / load (JSON under `experiments/`)  
- Dataset switching (`demo_lab`, `medium_enterprise`, custom)  

### Visualization

- Dark, minimal, technical cybersecurity UI  
- Interactive graph: zoom, pan, select, path highlight  
- Gravity-colored nodes and well markers  
- Dashboard statistics and distribution charts  

### Data

- JSON dataset import  
- Synthetic lab graphs only (no real enterprise data shipped)  

---

## 9. Installation

### Prerequisites

- Python 3.12 or 3.13  
- Node.js 18–22 (Node 22 LTS recommended)  
- npm 10+ (if system npm is broken, use nvm)  

### Automated install

```bash
cd cerberus-gravity
chmod +x install.sh start-backend.sh start-frontend.sh
./install.sh
```

### Manual install

**Backend**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

**Frontend**

```bash
# If npm reports "LRU is not a constructor", fix Node first:
export NVM_DIR="$HOME/.config/nvm"   # or $HOME/.nvm
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 22 && nvm use 22

cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

---

## 10. Quick Start

**Terminal 1 — API**

```bash
./start-backend.sh
# or:
cd backend && source .venv/bin/activate
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — UI**

```bash
./start-frontend.sh
# or:
cd frontend && npm run dev
```

| Service | URL |
|---------|-----|
| Dashboard | http://127.0.0.1:3000 |
| API | http://127.0.0.1:8000 |
| OpenAPI docs | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

Health check:

```bash
curl http://127.0.0.1:8000/api/v1/analysis/health
```

Full analysis:

```bash
curl "http://127.0.0.1:8000/api/v1/analysis/full?entry=inet-01&objective=crit-01"
```

---

## 11. Docker Setup

```bash
docker compose up --build
```

- Backend: port `8000`  
- Frontend service is defined for Node-based dev; adjust env `NEXT_PUBLIC_API_URL` as needed  

Environment template: `.env.example`

```
SECRET_KEY=change-me-in-production
DATABASE_URL=sqlite+aiosqlite:///./cerberus.db
DEBUG=true
```

---

## 12. Demo & Datasets

All shipped graphs are **synthetic**.

| Dataset | Description |
|---------|-------------|
| `demo_lab.json` | Small lab: Internet → Web → App → DB / Identity → Critical Server |
| `medium_enterprise.json` | Mid-size synthetic enterprise (DMZ, app tier, data tier, identities, jump host) |

Load via API:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analysis/load/demo_lab
curl -X POST http://127.0.0.1:8000/api/v1/analysis/load/medium_enterprise
```

List datasets:

```bash
curl http://127.0.0.1:8000/api/v1/analysis/datasets
```

### Dataset schema (JSON)

```json
{
  "name": "Example Lab",
  "description": "Synthetic only",
  "version": "1.0",
  "assets": [
    {
      "id": "web-01",
      "name": "Web Server",
      "type": "server",
      "ip": "10.0.1.10",
      "hostname": "web01.lab",
      "criticality": 55.0,
      "privilege_level": 40.0,
      "reachability": 85.0,
      "exposure": 80.0,
      "trust_level": 40.0,
      "business_value": 60.0
    }
  ],
  "identities": [],
  "relationships": [
    {
      "source": "inet-01",
      "target": "web-01",
      "relationship_type": "access",
      "trust": 20.0,
      "permission": "http",
      "distance": 1.0,
      "confidence": 0.95
    }
  ]
}
```

---

## 13. Graph Model

### Nodes

- **Assets** — servers, workstations, databases, network edges, etc.  
- **Identities** — users / privileged accounts modelled as graph nodes  

### Edges

Typed directed relationships, for example:

- `access`  
- `dependency`  
- `trust`  
- `communication`  
- `privilege_escalation`  
- `admin_access`  

Edge attributes: `trust`, `permission`, `distance`, `confidence`.

### Construction

`GraphEngine` builds a NetworkX `DiGraph`, supports clone (for what-if), attribute updates, and serializable export.

---

## 14. Gravity Algorithm

1. Load assets and relationships into the graph.  
2. Compute raw / combined gravity per asset (`GravityEngine`).  
3. Write `gravity` onto node attributes.  
4. Optionally propagate influence (`GravityPropagator`).  
5. Detect wells above a threshold (default 70).  
6. Compute centralities and strategic criticality.  
7. Rank paths and blast radii as requested.  

Weights and propagation parameters are runtime-configurable.

---

## 15. Attack Path Algorithm

1. Select entry points and an objective node.  
2. Enumerate simple paths (cutoff-limited for tractability).  
3. Score each path (distance, gravity, risk, strategic attraction, etc.).  
4. Rank by mode:

| Mode | Objective |
|------|-----------|
| `shortest` | Minimize hops |
| `highest_gravity` | Maximize path gravity |
| `lowest_risk` | Minimize experimental risk |
| `strategic` | Maximize strategic attraction |

Default UI/API mode: **strategic**.

---

## 16. Research Mode

Researchers can:

1. Adjust gravity weights via sliders (UI) or API.  
2. Recompute gravity and paths.  
3. Save experiment snapshots (configuration + results).  
4. Compare runs offline using files under `experiments/`.  

Example weight update:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analysis/weights \
  -H "Content-Type: application/json" \
  -d '{"asset_value_weight":1.0,"privilege_weight":1.5,"reachability_weight":1.0,"trust_weight":0.8,"exposure_weight":1.1}'
```

---

## 17. Experiments

Experiments are stored as JSON in `experiments/`.

```bash
# Save
curl -X POST http://127.0.0.1:8000/api/v1/analysis/experiments \
  -H "Content-Type: application/json" \
  -d '{"name":"Decay study A","configuration":{"weights":{"privilege_weight":1.5}}}'

# List
curl http://127.0.0.1:8000/api/v1/analysis/experiments
```

Each record includes: `id`, `name`, `configuration`, `dataset`, `results`, `created_at`.

---

## 18. API Documentation

Interactive docs: **http://127.0.0.1:8000/docs**

### Selected endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Project metadata |
| `GET` | `/api/v1/analysis/health` | Health + node count |
| `GET` | `/api/v1/analysis/full` | Full analysis pipeline |
| `GET` | `/api/v1/analysis/gravity` | Gravity map |
| `GET` | `/api/v1/analysis/blast/{node_id}` | Blast radius |
| `POST` | `/api/v1/analysis/remediate` | Remediation simulation |
| `POST` | `/api/v1/analysis/what-if` | Batch what-if changes |
| `POST` | `/api/v1/analysis/weights` | Update gravity weights |
| `POST` | `/api/v1/analysis/load/{name}` | Load dataset |
| `GET` | `/api/v1/analysis/datasets` | List datasets |
| `POST` | `/api/v1/analysis/experiments` | Save experiment |
| `GET` | `/api/v1/analysis/experiments` | List experiments |
| `GET` | `/api/v1/graph/` | Export nodes + edges |

### Remediation actions

- `reduce_privilege`  
- `reduce_exposure`  
- `reduce_criticality`  
- `remove_outbound_trust`  
- `increase_segmentation`  

Responses include **before → after** values and percentage changes, labelled as modelled estimates.

---

## 19. Frontend Dashboard

| Route | Purpose |
|-------|---------|
| `/` | Main dashboard — stats, distribution, top assets, graph, paths |
| `/graph` | Full interactive attack graph + node inspector |
| `/paths` | Path list, metrics, path highlighting on graph |
| `/blast` | Blast radius explorer |
| `/remediate` | Remediation simulator UI |
| `/research` | Weight controls + experiment save |

Design language: dark, minimal, high-contrast, graph-centric. Avoids neon “hacker” aesthetics.

---

## 20. Project Structure

```
cerberus-gravity/
├── backend/
│   ├── app/
│   │   ├── api/v1/           # REST routes (analysis, graph)
│   │   ├── core/             # Settings
│   │   ├── models/           # SQLAlchemy entities
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # AnalysisService
│   │   ├── graph/            # Graph, paths, criticality, blast
│   │   ├── gravity/          # Gravity, propagation, metrics
│   │   ├── simulation/       # Reserved for extended sims
│   │   ├── analytics/        # Reserved for extended analytics
│   │   └── main.py           # FastAPI entry
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/                  # Next.js App Router pages
│   ├── components/
│   │   ├── dashboard/
│   │   ├── graph/
│   │   ├── layout/
│   │   └── ui/
│   ├── lib/                  # API client, utils
│   └── types/
├── datasets/
│   ├── demo_lab.json
│   └── medium_enterprise.json
├── experiments/              # Saved research runs
├── docs/
├── docker/
├── docker-compose.yml
├── install.sh
├── start-backend.sh
├── start-frontend.sh
├── .env.example
├── LICENSE
└── README.md
```

---

## 21. Testing

```bash
cd backend
source .venv/bin/activate
pip install pytest
PYTHONPATH=. pytest tests/ -v
```

Covered areas:

- Gravity computation and weight sensitivity  
- Graph load and gravity assignment  
- (Extend with path, blast, and API integration tests as needed)  

---

## 22. Limitations

- Gravity and risk scores are **experimental**, not standards.  
- Path enumeration uses a cutoff; very large graphs need sampling or heuristics.  
- Remediation and what-if results are **graph-model estimates**, not guarantees.  
- Authentication is minimal in local research mode; harden before any shared deployment.  
- Frontend expects the API at `http://127.0.0.1:8000` unless `NEXT_PUBLIC_API_URL` is set.  
- No live network discovery or exploitation is implemented (by design).  

---

## 23. Ethical Use

- Use **only** on systems and data you are authorized to analyze.  
- Prefer synthetic datasets and isolated labs.  
- Do not deploy against third-party networks without explicit permission.  
- Do not present CERBERUS scores as compliance or audit-grade risk ratings.  
- Document assumptions when publishing research that uses this tool.  

---

## 24. Future Work

- Richer experiment comparison UI (side-by-side runs)  
- Additional synthetic datasets (large enterprise)  
- Optional structured AI analysis assistant (non-autonomous, no invented graph data)  
- Persistent DB-backed multi-user research mode  
- Export to common graph formats (GraphML, GEXF)  
- Stronger authn/authz and rate limiting for shared deployments  

---

## 25. Author

**Sudeepa Wanigarathna**

CERBERUS GRAVITY is released as a cybersecurity research platform focused on correctness, reproducibility, explainability, and visualization of gravity-driven attack paths.

---

## 26. License

Copyright © 2026 Sudeepa Wanigarathna  

See [LICENSE](LICENSE) for terms.  

This software is provided for research and authorized defensive use. Metrics produced by the system are experimental research constructs and not industry-standard security scores.

---

*Built for serious cybersecurity research — correctness, reproducibility, explainability, and visualization first.*
