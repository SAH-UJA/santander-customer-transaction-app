# tests/test_routes.py

from myflaskapp.main import app

def test_app():
    test_client = app.test_client()
    api_resp = test_client.get("/")
    
    assert api_resp.status_code == 200
    assert api_resp.json == {"message": "OK"}
