from app import create_app

def client():
    app = create_app()
    app.config["APP_CONFIG"].api_key = "K"  # temporary override for testing
    return app.test_client()

def test_predict_ok():
    c = client()
    r = c.post("/predict",
               json={"features":[5.1,3.5,1.4,0.2], "id":"r1"},
               headers={"x-api-key":"K"})
    assert r.status_code == 200, r.get_json()

def test_predict_missing_key():
    c = client()
    r = c.post("/predict", json={"features":[5.1,3.5,1.4,0.2]})
    assert r.status_code == 401, r.get_json()

def test_predict_bad_length():
    c = client()
    r = c.post("/predict",
               json={"features":[1,2,3]},
               headers={"x-api-key":"K"})
    assert r.status_code == 400, r.get_json()
