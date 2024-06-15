import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the jobs API.

    Attributes:
        app_name (str): The name of the application.
        debug (bool): Flag indicating whether debug mode is enabled.
        description (str): A description of the API service.
        database_url (str): The URL of the database.

    """

    app_name: str = "jobs"
    debug: bool = False
    description: str = "An API providing a service that manages job postings."
    database_url: str

    class Config:
        env_file = os.getenv("ENV_FILE", None)
