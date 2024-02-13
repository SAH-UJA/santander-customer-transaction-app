"""
Module for Santander Customer Transaction Prediction API endpoints related to inference.

This module defines API endpoints for batch inference on customer transaction data.
"""

from utils.config_reader import classification_config
from server.core.model_loader import PredictionModel
from fastapi import APIRouter, File, UploadFile
import pandas as pd
import tempfile
import json
import os


# Load prediction model
prediction_model = PredictionModel(
    os.path.join(os.getcwd(), classification_config["model_path"])
)

router = APIRouter(
    prefix=classification_config["api_prefix"],
    tags=classification_config["api_tags"],
    responses={404: {"description": "Not found"}},
)


@router.post("/uploadfile")
async def run_batch_inference(data_file: UploadFile = File(...)):
    """
    Endpoint for running batch inference on customer transaction data.
    """
    with tempfile.NamedTemporaryFile() as temp_file:
        contents = await data_file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name
        df = pd.read_csv(temp_file_path)
        results_df = prediction_model.perform_inference(df)
        resp = results_df.to_json(orient="records")
    return json.loads(resp)
