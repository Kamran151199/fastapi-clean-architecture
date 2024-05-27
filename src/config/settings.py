"""
This module contains the settings for the application.
"""

from pydantic import (
    PostgresDsn,
    Field,
    computed_field
)

from pydantic_settings import BaseSettings




class Settings(BaseSettings):
    """
    Application settings.
    """

    # Database settings
    pg_host: str = Field(..., alias="POSTGRES_HOST", env="POSTGRES_HOST")
    pg_port: int = Field(..., alias="POSTGRES_PORT", env="POSTGRES_PORT")
    pg_name: str = Field(..., alias="POSTGRES_DB", env="POSTGRES_DB")
    pg_user: str = Field(..., alias="POSTGRES_USER", env="POSTGRES_USER")
    pg_password: str = Field(..., alias="POSTGRES_PASSWORD", env="POSTGRES_PASSWORD")
    phantom_buster_api_key: str = Field(..., alias="PHANTOM_BUSTER_API_KEY", env="PHANTOM_BUSTER_API_KEY")
    phantom_buster_base_url: str = Field(..., alias="PHANTOM_BUSTER_BASE_URL", env="PHANTOM_BUSTER_BASE_URL")

    @computed_field
    def pg_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.pg_user,
            password=self.pg_password,
            host=self.pg_host,
            port=self.pg_port,
            path=self.pg_name or "",
        )

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = "src/.env"
        extra_forbidden = False


settings = Settings()