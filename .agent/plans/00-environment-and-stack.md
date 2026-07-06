# Plan 00: Environment and Local Stack

## Goal

Start and verify the local Docker Compose services required by Lab 28.

## Prerequisites

- Docker Desktop is running.
- Python 3.10+ is available.
- `.env` exists before starting `api-gateway` if the chat endpoint needs Kaggle URLs.

## Tasks

- Create or update local `.env` with placeholder-free runtime values when available.
- Start services with `docker compose up -d`.
- Verify Kafka, Prefect, Redis, Qdrant, Prometheus, Grafana, and API Gateway containers are running.
- Check service URLs:
  - Prefect: `http://localhost:4200`
  - Grafana: `http://localhost:3000`
  - Qdrant: `http://localhost:6333/dashboard`
  - Prometheus: `http://localhost:9090`
  - API Gateway: `http://localhost:8000/health`

## Verification

```powershell
docker compose ps
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:9090/-/healthy
Invoke-RestMethod http://localhost:3000/api/health
```

## Acceptance Criteria

- Required containers are up.
- API Gateway health endpoint returns `{"status":"ok"}`.
- Prometheus and Grafana health checks respond.
- No secrets are written into tracked files.

## Common Issues

- API Gateway may fail if `VLLM_NGROK_URL` is missing because `docker-compose.yml` maps it to `VLLM_URL`.
- Kafka topic checks may fail until data has been ingested.
- Port conflicts must be resolved before running the stack.
