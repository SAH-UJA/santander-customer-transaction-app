"""This module covers basic API I/O tests"""

from app.server.main import flask_app


def test_index_route():
    """Test to check basic output of home route"""
    response = flask_app.test_client().get('/')

    assert response.status_code == 200
