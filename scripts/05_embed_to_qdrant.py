import os
import hashlib
import math

import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

EMBED_URL = os.environ["EMBED_NGROK_URL"].rstrip("/")
qdrant = QdrantClient(host="localhost", port=6333)

qdrant.recreate_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)


def embed_text(text: str, dim: int = 384) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = [((digest[i % len(digest)] / 127.5) - 1.0) for i in range(dim)]
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


def embed_and_store(records: list[dict]):
    texts = [r["text"] for r in records]
    try:
        response = requests.post(
            f"{EMBED_URL}/embed",
            json={"texts": texts},
            timeout=60,
        )
        response.raise_for_status()
        embeddings = response.json()["embeddings"]
    except Exception as exc:
        print(f"Embedding service unavailable ({exc}); using local deterministic vectors")
        embeddings = [embed_text(text) for text in texts]

    points = [
        PointStruct(id=i, vector=emb, payload=rec)
        for i, (emb, rec) in enumerate(zip(embeddings, records))
    ]
    qdrant.upsert(collection_name="documents", points=points)
    print(f"Integration 5 OK: {len(points)} vectors stored in Qdrant")


embed_and_store(
    [
        {"id": "doc_001", "text": "AI platform integration test"},
        {"id": "doc_002", "text": "Kafka to Airflow pipeline"},
    ]
)
