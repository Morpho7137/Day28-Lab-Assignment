import json
import os
import subprocess
import time

from kafka import KafkaProducer

TOPIC = os.environ.get("KAFKA_TOPIC", "data.raw")
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")


def build_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        api_version=(2, 5, 0),
        request_timeout_ms=15000,
        max_block_ms=15000,
        value_serializer=lambda v: json.dumps(v).encode(),
    )


def ingest_via_docker(records: list[dict]):
    payload = "\n".join(json.dumps(record) for record in records)
    subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "kafka",
            "bash",
            "-lc",
            f"kafka-console-producer --bootstrap-server localhost:29092 --topic {TOPIC}",
        ],
        input=payload,
        text=True,
        check=True,
    )
    for record in records:
        print(f"Sent via Docker fallback: {record['id']}")


def ingest_data(records: list[dict]):
    try:
        producer = build_producer()
        for record in records:
            producer.send(TOPIC, value=record).get(timeout=15)
            print(f"Sent: {record['id']}")
        producer.flush()
        producer.close()
    except Exception as exc:
        print(f"Kafka host producer failed ({exc}); using Docker fallback")
        ingest_via_docker(records)


sample_data = [
    {"id": "doc_001", "text": "AI platform integration test", "timestamp": time.time()},
    {"id": "doc_002", "text": "Kafka to Airflow pipeline", "timestamp": time.time()},
]

ingest_data(sample_data)
print("Integration 1 OK: Data -> Kafka")
