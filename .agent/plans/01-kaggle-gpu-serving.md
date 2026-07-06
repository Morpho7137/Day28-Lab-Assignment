# Plan 01: Kaggle GPU Serving

## Goal

Run vLLM and embedding services on Kaggle GPU, expose them through ngrok or cloudflared, and provide URLs to the local stack.

## Prerequisites

- Kaggle notebook has GPU enabled.
- For ngrok: `NGROK_AUTH_TOKEN` is available.
- For cloudflared: no ngrok token is required.

## Tasks

- Run the Kaggle dependency installation cells from `LAB28_Huong_Dan.ipynb` or `kaggle-day28.ipynb`.
- Start vLLM with `Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4`.
- Expose the vLLM port with ngrok or cloudflared and record the public URL as `VLLM_NGROK_URL`.
- Start the embedding API using `BAAI/bge-small-en-v1.5`.
- Expose the embedding API and record the public URL as `EMBED_NGROK_URL`.
- Optionally log model-serving metadata to MLflow.

## Verification

```python
import requests

requests.get("http://localhost:8001/health").status_code
requests.post(
    f"{VLLM_URL}/v1/chat/completions",
    json={
        "model": "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4",
        "messages": [{"role": "user", "content": "Say hello"}],
    },
    timeout=30,
).json()
requests.post(f"{EMBED_URL}/embed", json={"texts": ["test"]}, timeout=30).json()
```

## Acceptance Criteria

- vLLM endpoint returns a chat completion.
- Embedding endpoint returns a 384-dimensional embedding.
- Local `.env` has valid `VLLM_NGROK_URL` and `EMBED_NGROK_URL`.
- Tokens and URLs are not committed.

## Common Issues

- vLLM dependency installation may require the fallback versions shown in the notebooks.
- Kaggle sessions can stop, which invalidates tunnel URLs.
- Free tunnels may add latency and cause timeout-sensitive tests to fail.
