import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "jobs"
    debug: bool = False
    description: str = "An API providing a service that manages job postings."
    database_url: str

    class Config:
        env_file = os.getenv("ENV_FILE", None)
