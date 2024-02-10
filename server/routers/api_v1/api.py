from server.routers.api_v1.endpoints import inference
from fastapi import APIRouter


api_router = APIRouter(dependencies=None)
api_router.include_router(inference.router)
