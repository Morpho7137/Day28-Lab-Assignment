# Lab 28 Planning Index

## Objective

Complete the Lab 28 full platform integration sprint end to end, from data ingestion through model serving, observability, smoke tests, readiness check, and submission evidence.

## Task Order

| Status | Plan | Purpose | Depends On |
|---|---|---|---|
| Pending | `plans/00-environment-and-stack.md` | Start and verify the local Docker Compose platform. | None |
| Pending | `plans/01-kaggle-gpu-serving.md` | Start vLLM, embedding API, tunnels, and optional MLflow on Kaggle. | None |
| Pending | `plans/02-data-pipeline.md` | Ingest records into Kafka and move them to Delta-style parquet with Prefect. | 00 |
| Pending | `plans/03-feature-and-vector-stores.md` | Populate Redis features and Qdrant vectors. | 01, 02 |
| Pending | `plans/04-api-gateway.md` | Validate FastAPI chat path, Qdrant search, vLLM call, and metrics. | 00, 01, 03 |
| Pending | `plans/05-observability-and-readiness.md` | Verify Prometheus, Grafana, optional LangSmith, MLflow evidence, and readiness score. | 04 |
| Pending | `plans/06-smoke-tests.md` | Run and fix the required end-to-end smoke tests. | 05 |
| Pending | `plans/07-submission-demo.md` | Prepare screenshots, demo flow, README checks, and final submission material. | 06 |

## External Values

Keep these in `.env` or notebook variables only:
- `VLLM_NGROK_URL`
- `EMBED_NGROK_URL`
- `NGROK_AUTH_TOKEN` if using ngrok
- `LANGCHAIN_API_KEY` and `LANGCHAIN_PROJECT` if validating LangSmith
- MLflow or DagsHub tracking credentials if using remote tracking

## Standard Verification Commands

```powershell
docker compose ps
python scripts/01_ingest_to_kafka.py
python scripts/03_delta_to_feast.py
python scripts/05_embed_to_qdrant.py
pytest smoke-tests/ -v
python scripts/production_readiness_check.py
```

## Final Acceptance Criteria

- All ten integration points from the lab document are demonstrably working.
- The five smoke-test groups pass.
- Production readiness score is above 80%.
- Required screenshots and README instructions are ready for submission.
- No secrets are committed.
