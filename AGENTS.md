# Repository Instructions

Address the user as sir and keep communication formal, direct, and focused on the task.

## Project Goal

Complete Lab 28 as a working hybrid AI platform:
- Local stack: Kafka, Prefect, Delta-style parquet storage, Redis feature store, Qdrant, FastAPI gateway, Prometheus, and Grafana.
- Kaggle stack: vLLM serving, embedding service, and optional MLflow tracking.
- Final acceptance: all integration points working, smoke tests passing, production readiness score above 80%, and submission artifacts prepared.

## Working Rules

- Read `.agent/PLANS.md` first, then follow the relevant task-specific plan in `.agent/plans/`.
- Keep work scoped to the current task plan unless a blocker requires a small supporting fix.
- Prefer existing repository scripts before adding new commands or abstractions.
- Do not commit or write real secrets, API keys, ngrok tokens, cloudflared URLs, LangSmith keys, or MLflow credentials.
- Store runtime secrets in local `.env` only. `.env` is ignored by Git.
- Use Windows-compatible commands when working in this workspace unless a command is explicitly for Kaggle or a container.
- Verify after every meaningful change with the command listed in the active plan.
- Preserve submission requirements from `SUBMISSION.md`: screenshots, smoke-test result, readiness score, README, and GitHub repo structure.

## Important External Inputs

The planning files can exist without external values, but a full end-to-end run requires:
- `VLLM_NGROK_URL` or a cloudflared vLLM tunnel URL.
- `EMBED_NGROK_URL` or a cloudflared embedding tunnel URL.
- `NGROK_AUTH_TOKEN` only when using ngrok.
- `LANGCHAIN_API_KEY` and `LANGCHAIN_PROJECT` only when validating LangSmith.
- MLflow or DagsHub credentials only when using remote MLflow tracking.

## Definition of Done

- `docker compose ps` shows the expected local services running.
- Kaggle vLLM and embedding endpoints are reachable from local.
- Kafka ingestion, Prefect processing, Redis features, and Qdrant vectors are verified.
- `pytest smoke-tests/ -v` passes.
- `python scripts/production_readiness_check.py` reports at least 80%.
- Submission evidence is collected and documented.
