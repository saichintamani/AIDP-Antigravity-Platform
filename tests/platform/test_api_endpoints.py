from fastapi.testclient import TestClient

from aidp.platform.api.main import app

client = TestClient(app)


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_spend_usd" in data
    assert "total_tokens_consumed" in data
    assert "research_throughput" in data
    assert "novel_discoveries" in data


def test_scheduler_queue_endpoint() -> None:
    response = client.get("/scheduler/queue")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "task_id" in data[0]


def test_launch_campaign_endpoint() -> None:
    payload = {"goal": "Find a cure for something.", "domain": "Biology"}
    response = client.post("/campaigns", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "campaign_id" in data

    # Check if we can retrieve it
    camp_id = data["campaign_id"]
    get_res = client.get(f"/campaigns/{camp_id}")
    assert get_res.status_code == 200
    assert get_res.json()["goal"] == "Find a cure for something."
