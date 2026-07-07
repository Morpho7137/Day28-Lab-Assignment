# Submission Notes

## What to submit

Submit the repository and five screenshots.

Screenshot list:

1. `prefect_ui.png`
2. `grafana_dashboard.png`
3. `api_gateway_chat.png`
4. `smoke_tests_results.png`
5. `production_readiness.png`

## Before taking screenshots

Make sure these are ready:

- Docker Desktop is running
- Kaggle URLs are already in `.env`
- the local virtual environment exists at `.venv`

If you need to start the stack:

```powershell
docker compose up -d --build
```

## Run order

### 1. Ingest sample data

```powershell
.\.venv\Scripts\python.exe scripts\01_ingest_to_kafka.py
```

### 2. Move Kafka data into parquet

```powershell
docker compose exec -T prefect-worker sh -lc "python -m pip install kafka-python pandas pyarrow >/tmp/pip-prefect.log 2>&1 && python /opt/prefect/flows/kafka_to_delta.py"
```

### 3. Load features into Redis

```powershell
.\.venv\Scripts\python.exe scripts\03_delta_to_feast.py
```

### 4. Load embeddings into Qdrant

```powershell
.\.venv\Scripts\python.exe scripts\05_embed_to_qdrant.py
```

## Checks to run before screenshots

### Observability

```powershell
.\.venv\Scripts\python.exe scripts\09_verify_observability.py
```

### Readiness

```powershell
.\.venv\Scripts\python.exe scripts\production_readiness_check.py
```

### Smoke tests

```powershell
.\.venv\Scripts\python.exe -m pytest smoke-tests -v
```

Expected result:

- readiness score: `10/10`
- smoke tests: `8 passed`

## How to take each screenshot

### 1. Prefect UI

Open `http://localhost:4200`.

Capture:
- the page title
- the left sidebar
- the flow or run list

### 2. Grafana

Open `http://localhost:3000`.

If login is required:
- username: `admin`
- password: `admin`

Capture:
- the Grafana page header
- the main panel area

### 3. API Gateway response

Run this in PowerShell:

```powershell
python -c "import requests; payload={'query':'What is platform engineering?','embedding':[0.1]*384}; resp=requests.post('http://localhost:8000/api/v1/chat', json=payload, timeout=60); print(resp.status_code); print(resp.text)"
```

Capture:
- the command
- the `200` status
- the JSON response

### 4. Smoke tests

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest smoke-tests -v
```

Capture the terminal when all tests have passed.

### 5. Production readiness

Run:

```powershell
.\.venv\Scripts\python.exe scripts\production_readiness_check.py
```

Capture the terminal when the final score is shown.

## Short notes for presentation

### Why Kafka?

It separates ingestion from downstream processing. If a later step fails, the data can be replayed from Kafka.

### Why use Kaggle?

The model side runs remotely, so the local machine only needs to handle orchestration, storage, and monitoring.

### What if Kaggle is unavailable?

The local stack can still start. Only the remote inference and embedding steps stop working.

### What if Kafka or Qdrant fails?

Only the dependent stage fails. The rest of the stack can still stay up.
