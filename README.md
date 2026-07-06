# Lab 28: Full Platform Integration Sprint

Hybrid AI platform using:
- Local Docker Compose for Kafka, Prefect, Redis, Qdrant, Prometheus, Grafana, and the FastAPI gateway
- Kaggle for remote chat and embedding services exposed through a tunnel

## Repository Layout

- `docker-compose.yml`: local platform stack
- `api-gateway/`: FastAPI gateway
- `prefect/flows/`: Kafka to Delta pipeline
- `scripts/`: integration, observability, and readiness scripts
- `smoke-tests/`: end-to-end smoke tests
- `kaggle-day28.ipynb`: patched Kaggle notebook for the remote services
- `LAB28_Huong_Dan.ipynb`: patched original lab notebook
- `.agent/`: planning files

## Prerequisites

- Docker Desktop running
- Python 3.11 available locally
- Kaggle notebook with internet enabled
- ngrok token configured in Kaggle secrets as `NGROK_AUTH_TOKEN`
- Valid LangSmith API key in local `.env`

## Local Environment

Create a local `.env` in the repository root with at least:

```env
VLLM_NGROK_URL=https://your-chat-tunnel.example
EMBED_NGROK_URL=https://your-embed-tunnel.example
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=lab28-platform
MLFLOW_TRACKING_URI=
MLFLOW_EXPERIMENT_NAME=lab28-integration
MLFLOW_TRACKING_USERNAME=
MLFLOW_TRACKING_PASSWORD=
QDRANT_URL=http://qdrant:6333
REDIS_URL=redis://redis:6379
```

## Kaggle Notebook

Use `kaggle-day28.ipynb` if Kaggle package installation is unstable.

Validated behavior:
- remote chat endpoint exposed at `/v1/chat/completions`
- remote embedding endpoint exposed at `/embed`

After running the notebook, copy the printed tunnel URLs into `.env`:
- `VLLM_NGROK_URL`
- `EMBED_NGROK_URL`

## Local Setup

Create and use a local virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r prefect\flows\requirements.txt redis qdrant-client requests python-dotenv pytest langsmith "numpy<2" "griffe<1"
```

Start the local stack:

```powershell
docker compose up -d --build
```

Services:
- API Gateway: `http://localhost:8000`
- Prefect UI: `http://localhost:4200`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Qdrant: `http://localhost:6333`

## Validated Execution Order

### 1. Ingest sample data to Kafka

```powershell
.\.venv\Scripts\python.exe scripts\01_ingest_to_kafka.py
```

Note:
- On this Windows environment, direct `kafka-python` producer access is unreliable.
- The script falls back to `docker compose exec kafka ... kafka-console-producer`.

### 2. Run Kafka to Delta

Validated path:

```powershell
docker compose exec -T prefect-worker sh -lc "python -m pip install kafka-python pandas pyarrow >/tmp/pip-prefect.log 2>&1 && python /opt/prefect/flows/kafka_to_delta.py"
```

This writes parquet files into `delta-lake/raw/`.

### 3. Push Delta records to Redis

```powershell
.\.venv\Scripts\python.exe scripts\03_delta_to_feast.py
```

### 4. Push embeddings to Qdrant

```powershell
.\.venv\Scripts\python.exe scripts\05_embed_to_qdrant.py
```

### 5. Verify API Gateway

```powershell
@'
import requests
payload = {"query": "What is platform engineering?", "embedding": [0.1] * 384}
resp = requests.post("http://localhost:8000/api/v1/chat", json=payload, timeout=60)
print(resp.status_code)
print(resp.text)
'@ | .\.venv\Scripts\python.exe -
```

## Validation

Observability:

```powershell
.\.venv\Scripts\python.exe scripts\09_verify_observability.py
```

Production readiness:

```powershell
.\.venv\Scripts\python.exe scripts\production_readiness_check.py
```

Smoke tests:

```powershell
.\.venv\Scripts\python.exe -m pytest smoke-tests -v
```

Validated result on this machine:
- `scripts/production_readiness_check.py`: `10/10 = 100%`
- `pytest smoke-tests -v`: `8 passed`

## Notes

- Prometheus does not scrape Kafka directly on `9092`; that was removed because Kafka is not an HTTP metrics endpoint there.
- The API Gateway formats retrieval context as plain text before sending it to the remote chat fallback service. Raw object-style context caused remote `404` responses.
- The local Prefect file remains deployable, but the validated execution path for this environment is the direct container-side run above.
