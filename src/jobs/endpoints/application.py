import logging
from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from .base import AbstractModel
from ..utils.application import ApplicationState


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/applications",
    tags=["applications"],
)


class ApplicationInput(BaseModel):
    """
    Represents the input data for an Application.

    Attributes:
        job_id (UUID): The unique identifier of the job associated with the application.
    """

    job_id: UUID


class Application(AbstractModel, ApplicationInput):
    """
    Represents the output data for an application.

    Attributes:
        state (ApplicationState): The state of the job.
        user_id (UUID): The unique identifier of the user associated with the application.
    """

    state: ApplicationState
    user_id: UUID


@router.patch("/{application_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def patch_application(application_id: UUID) -> None:
    """
    Update an application.

    Args:
        application_id (UUID): The ID of the application.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.get("/{application_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_application(application_id: UUID) -> None:
    """
    Retrieve a application.

    Args:
        application_id (UUID): The ID of the application.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.delete("/{application_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def delete_application(application_id: UUID) -> None:
    """
    Delete a application.

    Args:
        application_id (UUID): The ID of the application.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )
