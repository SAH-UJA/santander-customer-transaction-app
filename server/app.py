from server.core.config import settings
from server.routers.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI(
    title="Santander Customer Transactions Analytics",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    responses={
        500: {
            "description": "Internal Server Error"
        }
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def health():
    return {
        "message": "Santander Customer Transaction Analytics App Is Running..."
    }
