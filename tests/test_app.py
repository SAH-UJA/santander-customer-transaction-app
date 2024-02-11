"""
Test cases for the Santander Customer Transactions Analytics FastAPI application.

These test cases use the FastAPI TestClient to test the API endpoints for file upload functionality.
"""

from utils.config_reader import server_config, classification_config
from fastapi.testclient import TestClient
from server.app import app
from pathlib import Path
import os

# Initialize the TestClient
client = TestClient(app)


def test_upload_file():
    """
    Test the file upload endpoint with valid file data.

    Assertions:
    - Ensure the response status code is 200.
    - Ensure the response content matches the expected content for successful file upload.
    """
    # Prepare test data
    test_data_path = os.path.join(
        Path(__file__).parent, "test_data", "batch_of_two.csv"
    )
    files = {"data_file": ("batch_of_two.csv", open(test_data_path, "rb"))}

    # Make the API call
    route = (
        f"{server_config['api_prefix']}{classification_config['api_prefix']}/uploadfile"
    )
    response = client.post(route, files=files)

    # Assertions
    assert response.status_code == 200
    assert (
        response.content
        == b'[{"ID_code":"test_0","target_pred":1},{"ID_code":"test_1","target_pred":1}]'
    )


def test_upload_file_no_file():
    """
    Test the file upload endpoint without providing a file.

    Assertions:
    - Ensure the response status code is 422 (Unprocessable Entity).
    """
    # Make the API call without a file
    upload_route = (
        f"{server_config['api_prefix']}{classification_config['api_prefix']}/uploadfile"
    )
    response = client.post(upload_route)

    # Assertions
    assert response.status_code == 422
