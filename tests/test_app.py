from fastapi.testclient import TestClient
from server.app import app
from server.core.config import settings
import pytest

client = TestClient(app)

def test_upload_file():
    with open("test_file.txt", "w") as file:
        file.write("This is a test file.")

    files = {"file": ("test_file.txt", open("test_file.txt", "rb"))}
    route = f"{settings.API_V1_STR}/classification/inference/uploadfile"
    response = client.post(route, files=files)

    assert response.status_code == 200
    assert response.json() == {"filename": "test_file.txt"}

    # Clean up: Delete the test file
    if response.status_code == 200:
        file.close()
        import os
        os.remove("test_file.txt")

def test_upload_file_no_file():
    upload_route = f"{settings.API_V1_STR}/classification/inference/uploadfile"
    response = client.post(upload_route)
    
    assert response.status_code == 422