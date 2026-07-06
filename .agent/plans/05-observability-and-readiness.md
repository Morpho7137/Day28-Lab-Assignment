# Plan 05: Observability and Readiness

## Goal

Verify monitoring, optional tracing, MLflow evidence, and the production readiness score.

## Prerequisites

- Plan 04 is complete.
- API Gateway has handled at least one request so metrics exist.
- LangSmith values are available only if trace verification is required.

## Tasks

- Query Prometheus for API Gateway scrape status.
- Open or query Grafana health.
- Run `scripts/09_verify_observability.py` when LangSmith is configured.
- Confirm optional MLflow tracking evidence from Kaggle or local MLflow.
- Run `scripts/production_readiness_check.py`.
- Fix readiness blockers until the score is above 80%.

## Verification

```powershell
Invoke-RestMethod "http://localhost:9090/api/v1/query?query=up"
Invoke-RestMethod http://localhost:3000/api/health
python scripts/09_verify_observability.py
python scripts/production_readiness_check.py
```

## Acceptance Criteria

- Prometheus reports API Gateway as up.
- Grafana health endpoint responds.
- Readiness score is at least 80%.
- LangSmith check passes when `LANGCHAIN_API_KEY` is provided, or is documented as optional if not used.
- MLflow evidence is available if selected for the submission.

## Common Issues

- Prometheus metric names may differ from the query in the script.
- LangSmith cannot pass without a valid API key and project with at least one run.
- Kafka topic check depends on the actual Compose container name.
