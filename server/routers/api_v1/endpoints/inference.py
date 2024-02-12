"""
Module for Santander Customer Transaction Prediction API endpoints related to inference.

This module defines API endpoints for batch inference on customer transaction data.
"""

from utils.config_reader import classification_config
from fastapi import APIRouter, File, UploadFile
import pandas as pd
import numpy as np
import tempfile
import joblib
from pathlib import Path
import os
import lightgbm
import json


router = APIRouter(
    prefix=classification_config["api_prefix"],
    tags=classification_config["api_tags"],
    responses={404: {"description": "Not found"}},
)


def load_lightgbm_model():
    """
    Load the pre-trained LightGBM model.

    Returns:
        lightgbm.Booster: The loaded LightGBM model.
    """
    model_path = os.path.join(os.getcwd(), classification_config["model_path"])
    with open(model_path, "rb") as file:
        return joblib.load(file)


def perform_inference(df):
    """
    Perform inference using the loaded LightGBM model on the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing transaction data.

    Returns:
        pd.DataFrame: DataFrame with added 'target_pred' column based on the inference.
    """
    lgb_clf = load_lightgbm_model()
    pred = lgb_clf.predict(df[[f"var_{_}" for _ in range(200)]])
    df["target_pred"] = np.where(pred >= 0.5, 1, 0)
    return df[["ID_code", "target_pred"]][:100]


@router.post("/uploadfile")
async def run_batch_inference(data_file: UploadFile = File(...)):
    """
    Endpoint for running batch inference on customer transaction data.
    """
    try:
        with tempfile.NamedTemporaryFile() as temp_file:
            contents = await data_file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name
            df = pd.read_csv(temp_file_path)
            results_df = perform_inference(df)
            resp = results_df.to_json(orient="records")
        return json.loads(resp)
    except Exception as exc:
        return {
            "error": str(exc),
            "meta": os.path.join(os.getcwd(), classification_config["model_path"]),
            "exists": os.path.exists(
                os.path.join(os.getcwd(), classification_config["model_path"])
            ),
        }
