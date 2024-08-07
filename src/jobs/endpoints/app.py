"""
This module defines the FastAPI application for the jobs endpoints.

The FastAPI application is created with the specified title, description, debug settings, version, docs_url, and redoc_url attributes from the `Settings` class.

The `organization` router is included in the application to handle the jobs endpoints related to organizations.
"""

from fastapi import FastAPI

from .config import setup_logger
from ..endpoints import application, job, organization, user
from ..settings.base import Settings


settings = Settings()


app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    debug=settings.debug,
)
app.include_router(organization.router)
app.include_router(job.router)
app.include_router(user.router)
app.include_router(application.router)

setup_logger()
