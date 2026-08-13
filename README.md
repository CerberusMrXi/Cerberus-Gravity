# 🕸️ CERBERUS GRAVITY

**Risk-Weighted Attack Graph Intelligence Engine**

> Experimental cybersecurity research platform for studying how asset criticality, privilege, reachability, trust and graph structure influence attack-path risk.

**Author:** Sudeepa Wanigarathna  
**© 2026 Sudeepa Wanigarathna**

---

## Research Motivation

Traditional vulnerability scanners treat assets largely in isolation. CERBERUS GRAVITY models the insight that **high-value, highly privileged, highly reachable assets exert stronger influence on surrounding attack paths** — analogous to gravitational pull.

This platform constructs an attack graph and computes experimental metrics:

| Metric | Description |
|--------|-------------|
| **Asset Gravity** | Composite score from value × privilege × reachability × trust × exposure |
| **Path Gravity** | Aggregate gravity along an attack path |
| **Gravity Propagation** | Influence of high-gravity nodes on neighbors |
| **Gravity Wells** | High-attraction nodes or clusters |
| **Blast Radius** | Impact if a node is compromised |
| **Strategic Attraction** | Balanced path ranking |
| **Strategic Criticality** | Gravity + graph centralities |

> ⚠️ **All metrics are experimental research constructs.** They are **not** industry-standard risk scores and must not be treated as such.

---

## Architecture

```
CERBERUS GRAVITY
       │
 ┌─────┴─────┐
 │           │
Data      API Layer (FastAPI)
Ingestion    │
 │           ▼
 ▼      Graph Engine (NetworkX)
Asset        │
Discovery    ├─ Gravity Engine
 │           ├─ Path Engine
 ▼           └─ Risk / Simulation
Graph Construction
```

### Technology Stack

- **Backend:** Python 3.12, FastAPI, NetworkX, NumPy, Pydantic, SQLAlchemy
- **Frontend:** Next.js + React Flow (Phase 4+)
- **Deployment:** Docker / Docker Compose

---

## Gravity Model (Experimental)

```
raw ≈ ∏ (factor_i / 100) ^ weight_i

gravity = 100 × (1 − e^(−raw / 25))   // soft mapping to 0–100
```

Configurable weights:

- `asset_value_weight`
- `privilege_weight`
- `reachability_weight`
- `trust_weight`
- `exposure_weight`

Researchers can modify coefficients in Research Mode and compare experiments.

---

## Quick Start

### Prerequisites
- Python 3.12+
- Docker (optional)

### Local (without Docker)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
export PYTHONPATH=.
uvicorn app.main:app --reload --port 8000
```

Open: http://localhost:8000/docs

### Docker

```bash
docker compose up --build
```

API: http://localhost:8000  
Interactive docs: http://localhost:8000/docs

---

## Demo Dataset

A synthetic lab is loaded automatically:

```
Internet → Web Server → App Server → Database
                ↓
         User Workstation → Privileged Identity → Critical Server
```

All values are fictional.

---

## Key API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Project info |
| GET | `/api/v1/analysis/health` | Health check |
| GET | `/api/v1/analysis/full` | Full analysis (gravity, wells, paths, metrics) |
| GET | `/api/v1/analysis/gravity` | Gravity map |
| GET | `/api/v1/analysis/blast/{node_id}` | Blast radius |
| POST | `/api/v1/analysis/remediate` | Simulate remediation |
| POST | `/api/v1/analysis/weights` | Update gravity weights |
| POST | `/api/v1/analysis/what-if` | What-if simulation |
| GET | `/api/v1/graph/` | Full graph export |

Example:

```bash
curl "http://localhost:8000/api/v1/analysis/full?entry=inet-01&objective=crit-01"
```

---

## Project Structure

```
cerberus-gravity/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST endpoints
│   │   ├── core/            # Config
│   │   ├── models/          # SQLAlchemy entities
│   │   ├── schemas/         # Pydantic
│   │   ├── services/        # Orchestration
│   │   ├── graph/           # Graph, path, criticality, blast
│   │   ├── gravity/         # Gravity engine, propagation, metrics
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── datasets/                # Synthetic graphs (demo_lab.json)
├── docs/
├── docker/
├── docker-compose.yml
└── README.md
```

---

## Ethical Use

- Operate **only** against authorized lab environments, synthetic datasets, or isolated cyber ranges.
- Do **not** use for uncontrolled Internet exploitation or unauthorized systems.
- Remediation recommendations are **modelled estimates**, not guarantees.

---

## Limitations

- Gravity and risk scores are experimental research models.
- Path enumeration is limited by cutoff for large graphs.
- Frontend dashboard is planned for later phases.
- Authentication is minimal in research/demo mode.

---

## Future Work

- Interactive React Flow graph visualization
- Research Mode experiment storage & comparison
- Optional AI analysis assistant (structured, non-autonomous)
- Larger synthetic enterprise datasets
- Advanced what-if UI

---

## License

© 2026 Sudeepa Wanigarathna. All rights reserved.  
See LICENSE file for details.

---

*Built for serious cybersecurity research — correctness, reproducibility, explainability, and visualization first.*
