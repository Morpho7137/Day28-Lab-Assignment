# Plan 04: API Gateway

## Goal

Validate the FastAPI gateway for health, chat inference, vector search, error handling, and Prometheus metrics.

## Prerequisites

- Plans 00, 01, and 03 are complete.
- `VLLM_NGROK_URL` is set before starting the `api-gateway` container.
- Qdrant has the `documents` collection.

## Tasks

- Restart API Gateway after `.env` changes.
- Verify `/health`.
- Verify `/metrics`.
- Send a valid `/api/v1/chat` request with a 384-length embedding.
- Send an invalid request and confirm it returns a client error.
- Check that a timeout or tunnel failure does not keep the service unhealthy after the failed request.

## Verification

```powershell
docker compose up -d api-gateway
Invoke-RestMethod http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/metrics
Invoke-RestMethod -Method Post http://localhost:8000/api/v1/chat -ContentType "application/json" -Body '{"query":"What is platform engineering?","embedding":[0.1,0.1,0.1]}'
```

Use a full 384-length embedding for the real smoke-test request.

## Acceptance Criteria

- `/health` returns `ok`.
- `/metrics` is exposed.
- Valid chat request returns `answer`, `latency_ms`, and `model`.
- Invalid request returns `400` or `422`.
- Service remains healthy after timeout tests.

## Common Issues

- The current gateway expects `VLLM_URL`, mapped from `VLLM_NGROK_URL` in Compose.
- Short embeddings can cause Qdrant vector dimension errors.
- The smoke test expects latency below 2000 ms, which may be unrealistic over free tunnels.
