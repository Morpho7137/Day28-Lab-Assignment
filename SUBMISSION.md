# Submission Guide

## What to Submit

Repository contents:
- source code
- patched Kaggle notebook
- planning files under `.agent/`
- updated `README.md`

Screenshots to capture locally:
- Prefect UI at `http://localhost:4200`
- Grafana health or dashboard at `http://localhost:3000`
- API Gateway response from `http://localhost:8000/api/v1/chat`
- smoke test result
- production readiness result

## Recommended Screenshot Set

1. `prefect_ui.png`
2. `grafana_dashboard.png`
3. `api_gateway_chat.png`
4. `smoke_tests_results.png`
5. `production_readiness.png`

## Commands to Reproduce Before Submission

Start the stack:

```powershell
docker compose up -d --build
```

Run the validated pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\01_ingest_to_kafka.py
docker compose exec -T prefect-worker sh -lc "python -m pip install kafka-python pandas pyarrow >/tmp/pip-prefect.log 2>&1 && python /opt/prefect/flows/kafka_to_delta.py"
.\.venv\Scripts\python.exe scripts\03_delta_to_feast.py
.\.venv\Scripts\python.exe scripts\05_embed_to_qdrant.py
```

Run verification:

```powershell
.\.venv\Scripts\python.exe scripts\09_verify_observability.py
.\.venv\Scripts\python.exe scripts\production_readiness_check.py
.\.venv\Scripts\python.exe -m pytest smoke-tests -v
```

Expected result:
- readiness score: `100%`
- smoke tests: `8 passed`

## Short Technical Summary

- Kafka ingestion uses a Docker fallback on Windows because direct host producer access is unreliable in this stack.
- Kafka to Delta is executed inside `prefect-worker`, which has working broker resolution and writes parquet back to the repo volume.
- Remote Kaggle services are consumed through the URLs in `.env`.
- Prometheus, Grafana, Redis, Qdrant, and the API Gateway are all validated locally.

## Submission Questions

1. Architecture trade-offs:
   Balance was achieved by keeping GPU workloads remote on Kaggle while keeping orchestration, storage, and monitoring local. This reduces local hardware requirements but adds tunnel dependency risk.
2. Hybrid disconnection handling:
   The gateway and scripts are isolated from the local stack. If Kaggle is unavailable, local services still remain healthy, and the failure is contained to remote inference or embeddings.
3. Kafka decoupling:
   Kafka separates ingestion from downstream processing so data can be replayed and processed asynchronously.
4. Observability:
   Prometheus scrapes the API Gateway, Grafana visualizes health and metrics, and LangSmith receives trace submissions.
5. Failure handling:
   If Kafka or Qdrant fails, the stack degrades by failing only the dependent stage instead of collapsing the whole platform. Health endpoints and readiness checks make that visible quickly.
