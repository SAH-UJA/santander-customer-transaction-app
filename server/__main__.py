from server.core.config import settings
import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "server.app:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
