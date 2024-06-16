import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, validator

from ..services.organization import OrganizationService
from ..services.exceptions import ClientError, ConflictError, ServerError
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
        id (uuid.UUID): The unique identifier of the organization.
        name (str): The name of the organization.
        created (datetime): The datetime when the organization was created.
        updated (datetime): The datetime when the organization was last updated.
    """

    id: uuid.UUID
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
