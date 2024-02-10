from server.core.config import settings
from server.routers.api_v1.api import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request


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

app.mount("/static", StaticFiles(directory="server/static"), name="static")
templates = Jinja2Templates(directory="server/templates")

@app.get("/")
async def health():
    return {
        "message": "Santander Customer Transaction Analytics App Is Running..."
    }

@app.get("/ui")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
