# Plan 03: Feature and Vector Stores

## Goal

Populate Redis with feature records and Qdrant with document embeddings.

## Prerequisites

- Plans 01 and 02 are complete.
- `EMBED_NGROK_URL` is available in local environment.
- Redis and Qdrant are running.
- Delta-style parquet files exist.

## Tasks

- Run `scripts/03_delta_to_feast.py` to push features into Redis.
- Verify Redis has keys matching `feature:*`.
- Run `scripts/05_embed_to_qdrant.py` after exporting `EMBED_NGROK_URL`.
- Confirm Qdrant has a `documents` collection.
- Confirm the collection has points with 384-dimensional vectors.

## Verification

```powershell
python scripts/03_delta_to_feast.py
python scripts/05_embed_to_qdrant.py
Invoke-RestMethod http://localhost:6333/collections/documents
```

## Acceptance Criteria

- Redis contains one or more `feature:*` keys.
- Qdrant `documents` collection exists.
- Qdrant point count is greater than zero.
- Embedding service errors are surfaced clearly and not hidden.

## Common Issues

- `EMBED_NGROK_URL` must point to the public tunnel root, not `/embed`.
- Qdrant collection recreation can erase existing points.
- The script currently embeds fixed sample records, so it may not reflect every Kafka-ingested document.
