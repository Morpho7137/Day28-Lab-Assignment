import os
import time

import httpx
from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="AI Platform API Gateway")
Instrumentator().instrument(app).expose(app)

VLLM_URL = os.environ["VLLM_URL"]
QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant:6333")


class ChatRequest(BaseModel):
    query: str
    embedding: list[float] = Field(default_factory=lambda: [0.0] * 384)


def format_context(results: list[dict]) -> str:
    if not results:
        return "No retrieval context."

    lines = []
    for item in results:
        lines.append(f"doc_id={item.get('id')} score={item.get('score')}")
    return "\n".join(lines)


@app.post("/api/v1/chat")
async def chat(body: ChatRequest):
    start = time.time()

    async with httpx.AsyncClient(timeout=30) as client:
        search_resp = await client.post(
            f"{QDRANT_URL}/collections/documents/points/search",
            json={"vector": body.embedding, "limit": 3},
        )
        search_resp.raise_for_status()
        context = search_resp.json().get("result", [])
        prompt = f"Context:\n{format_context(context)}\n\nQuery: {body.query}"
        llm_resp = await client.post(
            f"{VLLM_URL}/v1/chat/completions",
            json={
                "model": "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4",
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        llm_resp.raise_for_status()

    latency = (time.time() - start) * 1000
    result = llm_resp.json()
    return {
        "answer": result["choices"][0]["message"]["content"],
        "latency_ms": round(latency, 2),
        "model": result["model"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
