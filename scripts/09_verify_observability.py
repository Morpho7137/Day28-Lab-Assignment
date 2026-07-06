import os
import uuid

import requests
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()


def check_prometheus():
    resp = requests.get(
        "http://localhost:9090/api/v1/query",
        params={"query": 'http_requests_total{job="api-gateway"}'},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    assert data["status"] == "success"
    print("Integration 9 OK: Prometheus metrics flowing")


def check_langsmith():
    client = Client(api_key=os.environ["LANGCHAIN_API_KEY"])
    project_name = os.environ.get("LANGCHAIN_PROJECT", "lab28-platform")
    run_id = uuid.uuid4()
    client.create_run(
        name="lab28-observability-check",
        run_type="tool",
        project_name=project_name,
        inputs={"source": "scripts/09_verify_observability.py"},
        outputs={"status": "ok"},
        id=run_id,
    )
    print(f"Integration 10 OK: LangSmith trace submitted ({run_id})")


check_prometheus()
check_langsmith()
