# Polyglot Commerce Integration Hub

Production-grade modernization of an academic Java + OCaml + Prolog e-commerce integration repository.

## Project Overview
This project transforms a legacy classroom implementation into a professional operations platform with:
- modular backend architecture,
- secure configuration handling,
- API-enabled quoting and order orchestration,
- interactive commercial dashboard,
- Docker and CI readiness.

## Business Problem
Organizations with polyglot legacy systems often keep business logic scattered across different languages and runtimes.

This platform consolidates pricing and order operations into a single service layer while preserving legacy assets for traceability.

## Architecture Diagram
```text
[Web Commerce Operations Board]
            |
            | REST JSON
            v
[FastAPI API Layer]
            |
            +--> [Pricing/Order Engine]
            |          |
            |          +--> category, loyalty, shipping rules
            |
            +--> [Prolog Data Loader]
            |
            +--> [Integration Status Probe]
                       |
                       +--> Java legacy files
                       +--> OCaml legacy files
                       +--> Prolog rules
```

## Tech Stack
- Python 3.11
- FastAPI + Uvicorn
- Vanilla HTML/CSS/JavaScript
- Pytest
- Docker + Docker Compose
- GitHub Actions CI

## Project Structure
```text
.
├── src/polyglot_commerce/
│   ├── api/
│   │   ├── app.py
│   │   ├── schemas.py
│   │   └── static/
│   ├── core/
│   │   ├── data.py
│   │   └── models.py
│   ├── engine/
│   │   └── service.py
│   └── utils/
├── tests/
├── scripts/
├── configs/
├── docs/
├── legacy/academic_project/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── .env.example
```

## Setup Instructions
### 1. Local setup
```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run application
```bash
./scripts/run_api.sh
```
Open `http://localhost:8080`.

### 3. Run tests
```bash
./scripts/test.sh
```

## API Endpoints
- `GET /health`
- `GET /api/integration`
- `GET /api/customers`
- `GET /api/items`
- `GET /api/orders`
- `GET /api/metrics`
- `GET /api/dashboard`
- `POST /api/quote`
- `POST /api/orders`
- `POST /api/reset`

Sample `POST /api/quote` payload:
```json
{
  "customer_id": 1,
  "lines": [
    { "item_id": 1, "quantity": 2 },
    { "item_id": 2, "quantity": 1 }
  ]
}
```

## CI/CD Overview
CI workflow (`.github/workflows/ci.yml`) validates every push/PR by:
- installing dependencies,
- running test suite,
- blocking regressions before merge.

Recommended CD:
- release tags for versioned deployments,
- container publish pipeline,
- deployment to managed container platform.

## Data Versioning Strategy
- Prolog rules are versioned in Git for reproducibility.
- For larger data assets, adopt DVC remote storage with tagged snapshots.

## Model Tracking Strategy
This project is rules-based (non-ML).
If ML is introduced (e.g., dynamic pricing models), integrate MLflow + DVC for full experiment/data lineage.

## Deployment Strategy
### Docker
```bash
docker compose up --build
```

### Runtime configuration
Defined by environment variables (`APP_HOST`, `APP_PORT`, `PROLOG_DATA_FILE`, etc.).

## Security Considerations
- no hardcoded credentials,
- `.env` excluded from source control,
- validated request schemas,
- integration probing without exposing sensitive paths externally.

## Lessons Learned
- polyglot legacy logic can be operationalized with a stable API facade,
- business-rule extraction from Prolog improves reproducibility,
- professional repo hygiene is essential for technical interviews.

## Future Improvements
- role-based authentication,
- persistent order storage (PostgreSQL),
- OpenAPI examples + contract tests,
- observability stack integration (Prometheus/Grafana),
- compatibility runners for Java/OCaml execution.

## Additional Technical Docs
- `docs/repository_audit.md`
- `docs/TECHNICAL_OVERVIEW.md`
- `docs/portfolio_ready.md`
