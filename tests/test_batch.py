from app import create_app

def test_batch_ok():
    app = create_app()
    app.config["APP_CONFIG"].api_key = "K"
    c = app.test_client()

    r = c.post("/batch_predict",
               json={"items":[
                   {"id":"r1","features":[5.1,3.5,1.4,0.2]},
                   {"id":"r2","features":[6.2,2.8,4.8,1.8]}
               ]},
               headers={"x-api-key":"K"})
    assert r.status_code == 200, r.get_json()
    body = r.get_json()
    assert "results" in body and len(body["results"]) == 2
