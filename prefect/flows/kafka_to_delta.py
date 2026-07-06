import json
import os
from datetime import datetime

import pandas as pd
from kafka import KafkaConsumer

try:
    from prefect import flow, task
except Exception:
    def task(fn):
        return fn

    def flow(*args, **kwargs):
        def decorator(fn):
            return fn
        return decorator

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
DELTA_PATH = os.environ.get("DELTA_PATH", "/opt/delta-lake/raw")


def _call_task(task_obj):
    return task_obj.fn() if hasattr(task_obj, "fn") else task_obj()


def _call_task_with_arg(task_obj, arg):
    return task_obj.fn(arg) if hasattr(task_obj, "fn") else task_obj(arg)


@task
def consume_and_process():
    consumer = KafkaConsumer(
        "data.raw",
        bootstrap_servers=KAFKA_BOOTSTRAP,
        api_version=(2, 5, 0),
        auto_offset_reset="earliest",
        consumer_timeout_ms=5000,
        value_deserializer=lambda m: json.loads(m.decode()),
    )
    records = [msg.value for msg in consumer]
    print(f"Consumed {len(records)} records from Kafka")
    return records


@task
def save_to_delta(records):
    if not records:
        print("No records to save")
        return

    os.makedirs(DELTA_PATH, exist_ok=True)
    df = pd.DataFrame(records)
    output_path = f"{DELTA_PATH}/batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    df.to_parquet(output_path)
    print(f"Saved {len(df)} records to Delta Lake: {output_path}")


@flow(name="Kafka to Delta Pipeline")
def kafka_to_delta_flow():
    records = consume_and_process()
    save_to_delta(records)


if __name__ == "__main__":
    run_mode = os.environ.get("PREFECT_FLOW_MODE", "run")
    if run_mode == "deploy":
        from prefect import flow as _prefect_flow  # noqa: F401
        kafka_to_delta_flow.deploy(
            name="kafka-to-delta",
            work_pool_name="lab28-worker",
        )
    else:
        records = _call_task(consume_and_process)
        _call_task_with_arg(save_to_delta, records)
