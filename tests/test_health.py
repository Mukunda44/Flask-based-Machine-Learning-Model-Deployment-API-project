from app import create_app

def test_health_ok():
    app = create_app()
    client = app.test_client()

    res = client.get("/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    body = res.get_json()
    assert "status" in body
