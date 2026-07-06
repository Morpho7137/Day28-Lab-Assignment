# Plan 02: Data Pipeline

## Goal

Move sample records from Kafka into Delta-style parquet storage through the Prefect flow.

## Prerequisites

- Plan 00 is complete.
- Kafka is reachable at `localhost:9092` for local scripts.
- Prefect services are running.

## Tasks

- Run `scripts/01_ingest_to_kafka.py` to publish sample records to the `data.raw` topic.
- Confirm the Kafka topic exists.
- Run or deploy `prefect/flows/kafka_to_delta.py`.
- Verify parquet files are written under the local `delta-lake/raw` path or the mounted container path.
- If path behavior differs between local and container execution, document the active path in the plan status.

## Verification

```powershell
python scripts/01_ingest_to_kafka.py
docker exec day28-lab-assignment-kafka-1 kafka-topics --list --bootstrap-server localhost:9092
python prefect/flows/kafka_to_delta.py
Get-ChildItem -Recurse delta-lake -ErrorAction SilentlyContinue
```

## Acceptance Criteria

- `data.raw` receives sample messages.
- Prefect flow consumes records without crashing.
- At least one parquet batch exists after processing.
- The flow can be rerun safely during smoke-test preparation.

## Common Issues

- The Kafka container name may differ by Compose project name.
- The flow uses `kafka:9092` inside containers, while local scripts use `localhost:9092`.
- The current flow writes to `/opt/delta-lake/raw` when run in a container.
