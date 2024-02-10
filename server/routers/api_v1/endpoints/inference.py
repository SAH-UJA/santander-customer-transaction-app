from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel


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
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
