"""
Santander Customer Transaction Inference App

This Streamlit application facilitates the inference of Santander customer transactions using a machine learning model hosted on an API.
Users can upload a CSV file containing transaction data, and the application will make an API call to obtain predictions based on the provided data.
"""

import streamlit as st
import requests
import ast
import logging
import os
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEPLOYED_TARGET: str = os.getenv(
    "DEPLOYED_TARGET", default="https://santander-customer-transaction-app.onrender.com"
)
BACKUP_TARGET: str = os.getenv(
    "BACKUP_TARGET",
    default="https://santander-customer-transaction-app-uat.onrender.com",
)
INFERENCE_ROUTE = "api/v1/classification/inference/uploadfile"
API_ENDPOINT = urljoin(DEPLOYED_TARGET, INFERENCE_ROUTE)


def call_api(file_contents, api_endpoint):
    """
    Call the API with the provided file contents.

    Parameters:
    - file_contents (bytes): Contents of the uploaded CSV file.
    - api_endpoint (str): API endpoint for making predictions.

    Returns:
    dict: API response in dictionary format.
    """
    try:
        # Prepare the file data
        files = {"data_file": ("filename", file_contents, "application/octet-stream")}

        # Make the API call
        response = requests.post(api_endpoint, files=files)  # Adjust timeout as needed

        # Check for successful response
        response.raise_for_status()

        # Return the response content
        return ast.literal_eval(response.content.decode("utf-8"))
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        return {"error": "API call failed"}


def is_primary_api_responsive():
    """
    Check if the primary API endpoint is responsive.

    Returns:
    bool: True if responsive, False otherwise.
    """
    try:
        response = requests.head(
            DEPLOYED_TARGET, timeout=30
        )  # Adjust timeout as needed
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def main():
    """
    Streamlit app for Santander Customer Transaction Inference.

    This function initializes the Streamlit app, handles file uploads, and triggers API calls based on user interactions.
    """
    global API_ENDPOINT

    st.title("Santander Customer Transaction Inference App")

    if not is_primary_api_responsive():
        st.warning("Primary API endpoint not responsive. Rolling back to backup.")

        # Use backup API endpoint
        DEPLOYED_TARGET = BACKUP_TARGET
        API_ENDPOINT = urljoin(DEPLOYED_TARGET, INFERENCE_ROUTE)

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file", type=["csv"], accept_multiple_files=False
    )

    if uploaded_file is not None:
        # Display uploaded file
        st.write("File Uploaded:", uploaded_file.name)

        # Button to trigger API call
        if st.button("Get Predictions"):
            # Read file contents
            file_contents = uploaded_file.read()

            # Call the API with the file contents
            api_response = call_api(file_contents, API_ENDPOINT)

            # Display API response
            st.write("API Response:")
            st.dataframe(api_response, width=800, height=400)


# Run the Streamlit app
if __name__ == "__main__":
    main()
