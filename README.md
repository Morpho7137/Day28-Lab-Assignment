# Day 28 Lab

This repo is the working version I used to get the lab running on Windows with Docker Desktop and a Kaggle notebook.

## What is in here

- docker-compose.yml: local services
- pi-gateway/: FastAPI gateway
- prefect/flows/: Kafka to parquet flow
- scripts/: small scripts for each integration step
- smoke-tests/: end-to-end checks
- kaggle-day28.ipynb: Kaggle notebook I used when package installs were unstable

## Before you start

You need:

- Docker Desktop running
- a local .env in the repo root
- Kaggle URLs already copied into .env

The important .env values are:

`env
VLLM_NGROK_URL=...
EMBED_NGROK_URL=...
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=lab28-platform
QDRANT_URL=http://qdrant:6333
REDIS_URL=redis://redis:6379
`

## Local Python

Use the local virtual environment:

`powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r prefect\flows\requirements.txt redis qdrant-client requests python-dotenv pytest langsmith "numpy<2" "griffe<1"
`

## Start the stack

`powershell
docker compose up -d --build
`

Main URLs:

- API Gateway: http://localhost:8000
- Prefect: http://localhost:4200
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Qdrant: http://localhost:6333

## Run order

### 1. Send sample data to Kafka

`powershell
.\.venv\Scripts\python.exe scripts\01_ingest_to_kafka.py
`

### 2. Move Kafka data into parquet

On this machine, the reliable way is to run it inside the worker container:

`powershell
docker compose exec -T prefect-worker sh -lc "python -m pip install kafka-python pandas pyarrow >/tmp/pip-prefect.log 2>&1 && python /opt/prefect/flows/kafka_to_delta.py"
`

That creates parquet files under delta-lake/raw/.

### 3. Load features into Redis

`powershell
.\.venv\Scripts\python.exe scripts\03_delta_to_feast.py
`

### 4. Load vectors into Qdrant

`powershell
.\.venv\Scripts\python.exe scripts\05_embed_to_qdrant.py
`

### 5. Check the chat endpoint

`powershell
python -c "import requests; payload={'query':'What is platform engineering?','embedding':[0.1]*384}; resp=requests.post('http://localhost:8000/api/v1/chat', json=payload, timeout=60); print(resp.status_code); print(resp.text)"
`

## Validation

Observability:

`powershell
.\.venv\Scripts\python.exe scripts\09_verify_observability.py
`

Readiness:

`powershell
.\.venv\Scripts\python.exe scripts\production_readiness_check.py
`

Smoke tests:

`powershell
.\.venv\Scripts\python.exe -m pytest smoke-tests -v
`

What passed on this machine:

- readiness: 10/10
- smoke tests: 8 passed

## Notes

- Kafka producer access from Windows was unreliable, so scripts/01_ingest_to_kafka.py has a Docker fallback.
- The API gateway sends plain text context to the remote chat service. Raw object formatting caused failures with the fallback Kaggle endpoint.
- I kept the Prefect flow file, but for this setup the container-side run is the dependable path.
