import logging
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from .base import AbstractModel
from ..utils.job import JobMode, JobContract, JobState


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["jobs"],
)


class JobInput(BaseModel):
    """
    Represents the input data for a job.

    Attributes:
        title (str): The title of the job.
        salary (float): The salary for the job.
        mode (JobMode): The mode of the job.
        contract (JobContract): The contract type for the job.
        description (str, optional): The description of the job. Defaults to None.
    """

    title: str
    salary: float
    mode: JobMode
    contract: JobContract
    description: str | None = None


class Job(AbstractModel, JobInput):
    """
    Represents the output data for a job.

    Attributes:
        state (JobState): The state of the job.
        organization_id (UUID): The unique identifier of the organization associated with the job.
    """

    state: JobState
    organization_id: UUID


@router.patch("/{job_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def patch_job(job_id: UUID) -> None:
    """
    Update a job.

    Args:
        job_id (UUID): The ID of the job.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.get("/{job_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_job(job_id: UUID) -> None:
    """
    Retrieve a job.

    Args:
        job_id (UUID): The ID of the job.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.delete("/{job_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def delete_job(job_id: UUID) -> None:
    """
    Delete a job.

    Args:
        job_id (UUID): The ID of the job.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.get("/{job_id}/applications", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_applications_by_job(job_id: UUID) -> None:
    """
    Retrieve applications for a job.

    Args:
        job_id (UUID): The ID of the job.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )
