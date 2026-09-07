"""Application configuration."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    """Settings loaded from environment variables and the project .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment settings
    ENVIRONMENT: str = Field(
        default="development", validation_alias="ENVIRONMENT"
    )
    LOG_LEVEL: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # Agent settings
    PROVIDER: str = Field(default="openai", validation_alias="PROVIDER")
    MODEL_NAME: str = Field(..., validation_alias="MODEL_NAME")
    API_BASE_URL: str = Field(..., validation_alias="API_BASE_URL")
    APIM_API_KEY: str = Field(..., validation_alias="APIM_API_KEY")
    RETRIEVER_PROMPT: Path = Field(..., validation_alias="RETRIEVER_PROMPT")
    REPORT_GENERATOR: Path = Field(..., validation_alias="REPORT_GENERATOR")

    # Knowledge-base settings
    KB_PATH: Path = Field(..., validation_alias="KB_PATH")
    CHUNKS_PATH: Path = Field(..., validation_alias="CHUNKS_PATH")
    CHUNK_SIZE: int = Field(default=500, validation_alias="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=50, validation_alias="CHUNK_OVERLAP")


settings = Settings()
