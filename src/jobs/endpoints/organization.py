import logging
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, validator

from .job import JobInput, JobOutput
from ..services.job import JobService
from ..services.organization import OrganizationService
from ..services.exceptions import ClientError, ConflictError, NotFoundError, ServerError
from ..utils.password import PASSWORD_SCHEMA, InvalidPasswordError


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/organizations",
    tags=["organizations"],
)


class OrganizationInput(BaseModel):
    """
    Represents the input data for an organization.

    Attributes:
        name (str): The name of the organization.
        password (str): The password for the organization.
    """

    name: str
    password: str

    @validator("password")
    def validate_password(cls, password: str) -> str:
        """
        Validate the password.

        Args:
            password (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password is empty.
        """
        if not PASSWORD_SCHEMA.validate(password):
            raise InvalidPasswordError()

        return password


class OrganizationOutput(BaseModel):
    """
    Represents the output data for an organization.

    Attributes:
        id (UUID): The unique identifier of the organization.
        name (str): The name of the organization.
        created (datetime): The datetime when the organization was created.
        updated (datetime): The datetime when the organization was last updated.
    """

    id: UUID
    name: str
    created: datetime
    updated: datetime


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_input: OrganizationInput,
) -> OrganizationOutput:
    """
    Create a new organization.

    Args:
        organization (OrganizationInput): The input data for creating the organization.

    Returns:
        OrganizationOutput: The created organization.

    Raises:
        HTTPException: If there is a conflict, bad request, or internal server error.
    """
    try:
        logger.info(f"Creating organization with name: {organization_input.name}")
        organization = OrganizationService().create(
            name=organization_input.name, password=organization_input.password
        )
    except ConflictError as exc:
        logger.error(f"Failed to create organization: {exc.message}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    except ClientError as exc:
        logger.error(f"Failed to create organization: {exc.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    except ServerError as exc:
        logger.error(f"Failed to create organization: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    logger.info(f"Organization created: {organization.name}")

    return OrganizationOutput(
        id=organization.id,
        name=organization.name,
        created=organization.created,
        updated=organization.updated,
    )


@router.post("/{organization_id}/jobs", status_code=status.HTTP_201_CREATED)
async def create_job(
    organization_id: UUID,
    job_input: JobInput,
) -> JobOutput:
    """
    Create a new job.

    Args:
        organization_id (UUID): The ID of the organization.
        job_input (JobInput): The input data for creating the job.

    Returns:
        JobOutput: The created job.

    Raises:
        HTTPException: If there is a conflict, bad request, or internal server error.
    """
    try:
        logger.info(
            f"Creating job with title: {job_input.title} (organization: {organization_id})."
        )
        job = JobService().create(
            organization_id=organization_id,
            title=job_input.title,
            salary=job_input.salary,
            mode=job_input.mode,
            contract=job_input.contract,
            description=job_input.description,
        )
    except NotFoundError as exc:
        logger.error(f"Failed to create job: {exc.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except ClientError as exc:
        logger.error(f"Failed to create job: {exc.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    except ServerError as exc:
        logger.error(f"Failed to create job: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    logger.info(f"Job created: {job.title} (organization: {organization_id}).")

    return JobOutput(
        id=job.id,
        title=job.title,
        salary=job.salary,
        mode=job.mode.value,
        contract=job.contract.value,
        description=job.description,
        organization_id=job.organization_id,
        state=job.state.value,
        created=job.created,
        updated=job.updated,
    )
