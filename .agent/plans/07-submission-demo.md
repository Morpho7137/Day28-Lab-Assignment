# Plan 07: Submission and Demo

## Goal

Prepare the final artifacts required by `SUBMISSION.md`.

## Prerequisites

- Plan 06 is complete.
- Smoke-test and readiness outputs are available.
- Local dashboards are accessible.

## Tasks

- Capture screenshots:
  - Prefect UI with flow evidence.
  - API Gateway health or chat call.
  - Grafana dashboard.
  - Smoke-test result.
  - Production readiness score.
- Verify README contains startup, flow deployment, smoke-test, and dashboard instructions.
- Prepare answers to the five submission questions:
  - Architecture trade-offs.
  - Local and Kaggle disconnect handling.
  - Kafka event-driven decoupling.
  - Logs, metrics, and traces.
  - Service crash and graceful degradation.
- Rehearse the demo flow: architecture overview, happy path, error scenario, observability, and Q&A.
- Confirm the final GitHub repository structure matches `SUBMISSION.md`.

## Verification

```powershell
pytest smoke-tests/ -v
python scripts/production_readiness_check.py
docker compose ps
```

## Acceptance Criteria

- Required screenshots exist.
- Smoke tests show passing results.
- Readiness score is above 80%.
- README is accurate for the final setup.
- No `.env` or secret material is included in the submission.

## Common Issues

- Dashboards need live traffic before graphs look meaningful.
- Kaggle kernels and tunnels must stay active during the demo.
- Submission screenshots should show enough context to prove the service and result.
