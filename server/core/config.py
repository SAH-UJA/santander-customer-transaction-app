from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    API_V1_STR: str = "/api/v1"


settings = Settings()
