from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str

    api_title: str = "NZ Louis Property API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api"

    max_page_size: int = 50
    default_page_size: int = 9
    query_timeout: int = 15

    cors_origins: list[str] = [
        "http://localhost:3000",
        "https://nzlouis-property-ai.vercel.app"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
