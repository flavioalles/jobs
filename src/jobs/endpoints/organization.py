import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..services.organization import OrganizationService
from ..services.exceptions import ClientError, ConflictError, ServerError


router = APIRouter(
    prefix="/api/v1/organizations",
    tags=["organizations"],
)


class OrganizationInput(BaseModel):
    """
    Represents the input data for an organization.

    Attributes:
        name (str): The name of the organization.
    """

    name: str


class OrganizationOutput(OrganizationInput):
    """
    Represents the output data for an organization.

    Attributes:
        id (uuid.UUID): The unique identifier of the organization.
        created (datetime): The datetime when the organization was created.
        updated (datetime): The datetime when the organization was last updated.
    """

    id: uuid.UUID
    created: datetime
    updated: datetime


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(organization: OrganizationInput) -> OrganizationOutput:
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
        organization = OrganizationService().create(organization.name)
    except ConflictError as exc:
        # TODO: log
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    except ClientError as exc:
        # TODO: log
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    except ServerError as exc:
        # TODO: log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    return OrganizationOutput(
        name=organization.name,
        id=organization.id,
        created=organization.created,
        updated=organization.updated,
    )
