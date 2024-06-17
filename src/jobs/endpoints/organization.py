import logging
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, validator

from .base import AbstractModel, PasswordInput, Token
from .job import JobInput, Job
from ..services.job import JobService
from ..services.organization import OrganizationService
from ..services.exceptions import ClientError, ConflictError, NotFoundError, ServerError
from ..utils.auth import (
    create_jwt_token,
    get_jwt_subject,
    FailedJWTDecodeError,
    NoJWTSubjectError,
)
from ..utils.password import PASSWORD_SCHEMA, InvalidPasswordError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/organizations/token")

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/organizations",
    tags=["organizations"],
)


class OrganizationInput(PasswordInput):
    """
    Represents the input data for an organization.

    Attributes:
        name (str): The name of the organization.
    """

    name: str


class Organization(AbstractModel):
    """
    Represents the output data for an organization.

    Attributes:
        name (str): The name of the organization.
    """

    name: str


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_input: OrganizationInput,
) -> Organization:
    """
    Create a new organization.

    Args:
        organization (OrganizationInput): The input data for creating the organization.

    Returns:
        Organization: The created organization.

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

    return Organization(
        id=organization.id,
        name=organization.name,
        created=organization.created,
        updated=organization.updated,
    )


@router.post("/auth", status_code=status.HTTP_200_OK)
async def authenticate_organization(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Authenticate an organization.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends()]): The form data containing the username and password.

    Returns:
        Token: The token for the authenticated organization.

    Raises:
        HTTPException: If there is a failure to authenticate.
    """
    try:
        logger.info(f"Authenticating organization {form_data.username}.")
        organization = OrganizationService().authenticate(
            name=form_data.username, password=form_data.password
        )
    except (NotFoundError, InvalidPasswordError) as exc:
        logger.error(f"Failed to authenticate organization: {exc.message}")
        # NOTE: not a good practice to return detailed error messages in this use case.
        # Hence, avoiding returning the actual error message.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failure to authenticate."
        )

    logger.info(f"Authenticated organization {form_data.username}.")

    return Token(access_token=create_jwt_token(organization.name))


async def get_authenticated_organization(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> Organization:
    """
    Retrieves the authenticated organization based on the provided token.

    Args:
        token (str): The authentication token.

    Returns:
        Organization: The authenticated organization.

    Raises:
        HTTPException: If the token is invalid or the organization cannot be retrieved.
    """
    try:
        organization = OrganizationService().get(name=get_jwt_subject(token))
    except (FailedJWTDecodeError, NoJWTSubjectError, NotFoundError) as exc:
        logger.error(f"Failed to decode JWT token/get Organization: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Organization(
        id=organization.id,
        name=organization.name,
        created=organization.created,
        updated=organization.updated,
    )


@router.post("/{organization_id}/jobs", status_code=status.HTTP_201_CREATED)
async def create_job(
    organization_id: UUID,
    job_input: JobInput,
    authenticated_organization: Annotated[
        Organization, Depends(get_authenticated_organization)
    ],
) -> Job:
    """
    Create a new job.

    Args:
        organization_id (UUID): The ID of the organization.
        job_input (JobInput): The input data for creating the job.

    Returns:
        Job: The created job.

    Raises:
        HTTPException: If there is a conflict, bad request, or internal server error.
    """
    if organization_id != authenticated_organization.id:
        logger.error(
            f"Failed to create job: Organization mismatch (path: {organization_id}, authenticated: {authenticate_organization.id})."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Failed to create job: Organization mismatch.",
        )

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

    return Job(
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
