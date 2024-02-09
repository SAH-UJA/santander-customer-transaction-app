from app.server.main import flask_app


def test_index_route():
    response = flask_app.test_client().get('/')

    assert response.status_code == 200
    assert response.json == {"message": "OK"}
