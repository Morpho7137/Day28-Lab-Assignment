# Plan 06: Smoke Tests

## Goal

Run and pass the required smoke tests in `smoke-tests/test_e2e.py`.

## Prerequisites

- Plans 00 through 05 are complete.
- API Gateway, Prometheus, Grafana, Kafka, Redis, and Qdrant are running.
- Kaggle vLLM tunnel is active.
- Qdrant and Redis contain data.

## Tasks

- Run the full smoke-test suite.
- If failures occur, classify them by group:
  - Happy path: API Gateway, Qdrant, or vLLM.
  - Data ingestion: Kafka or Qdrant population.
  - Observability: Prometheus or Grafana.
  - Failure path: invalid request or post-timeout health.
  - Feature store: Redis data.
- Fix the smallest blocker that restores the expected integration behavior.
- Rerun the full suite after fixes.

## Verification

```powershell
pytest smoke-tests/ -v
```

## Acceptance Criteria

- All smoke tests pass.
- Test output is captured for submission evidence.
- Any environment-specific assumptions are documented in `.agent/PLANS.md`.

## Common Issues

- Smoke tests rely on existing Qdrant and Redis data.
- Free tunnel latency may violate the `latency_ms < 2000` assertion.
- The ingestion test sends Kafka data but does not itself run the embedding script.
