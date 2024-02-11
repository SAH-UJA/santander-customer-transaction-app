"""
Main module for the Santander Customer Transactions Analytics FastAPI application.

This module sets up the FastAPI application, including configuration, middleware, routers, and health check endpoint.
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from utils.config_reader import server_config
from server.routers.api_v1.api import api_router

# Create a FastAPI application
app = FastAPI(
    title="Santander Customer Transactions Analytics",
    openapi_url=f'{server_config["api_prefix"]}/openapi.json',
    docs_url=f'{server_config["api_prefix"]}/docs',
    responses={500: {"description": "Internal Server Error"}},
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# Include API routers
app.include_router(api_router, prefix=server_config["api_prefix"])


@app.get("/")
async def health():
    """
    Health check endpoint.
    """
    return {"message": "Santander Customer Transaction Analytics App Is Running..."}


@app.head("/")
async def monitor():
    """
    Monitor endpoint.
    """
    return {"message": "Santander Customer Transaction Analytics App Is Running..."}
