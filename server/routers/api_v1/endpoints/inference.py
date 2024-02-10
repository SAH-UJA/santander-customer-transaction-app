from fastapi import APIRouter, File, UploadFile
import pandas as pd
import numpy as np
import tempfile
import pickle
from pathlib import Path
import os
import lightgbm
import json


router = APIRouter(
    prefix="/classification/inference",
    tags=["Santander Customer Transaction Prediction"],
    responses={
        404: {
            "description": "Not found"
        }
    }
)

@router.post("/uploadfile")
async def run_batch_inference(data_file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile() as temp_file:
        contents = await data_file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name
        df = pd.read_csv(temp_file_path)
        model_path = os.path.join(Path(__file__).resolve().parent.parent.parent.parent, "model", "lgb_clf.pkl")
        with open(model_path, 'rb') as file:
            lgb_clf = pickle.load(file)
        pred = lgb_clf.predict(df[[f"var_{_}" for _ in range(200)]])
        df["target_pred"] = np.where(pred >= 0.5, 1, 0)
        resp = df[["ID_code", "target_pred"]][:100].to_json(orient="records")
    return json.loads(resp)
