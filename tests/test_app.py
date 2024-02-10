from fastapi.testclient import TestClient
from server.core.config import settings
from server.app import app
from pathlib import Path
import os
import pytest

client = TestClient(app)

def test_upload_file():
    test_data_path = os.path.join(Path(__file__).parent, "test_data.csv")
    files = {"data_file": ("test_data.csv", open(test_data_path, "rb"))}
    route = f"{settings.API_V1_STR}/classification/inference/uploadfile"
    response = client.post(route, files=files)

    assert response.status_code == 200
    assert response.content == b'[{"ID_code":"test_0","target_pred":1},{"ID_code":"test_1","target_pred":1}]'


def test_upload_file_no_file():
    upload_route = f"{settings.API_V1_STR}/classification/inference/uploadfile"
    response = client.post(upload_route)
    
    assert response.status_code == 422
