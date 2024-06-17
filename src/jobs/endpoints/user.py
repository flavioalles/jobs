import logging
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, validator

from .base import AbstractModel, PasswordInput
from ..services.user import UserService
from ..services.exceptions import ClientError, ConflictError, NotFoundError, ServerError
from ..utils.password import PASSWORD_SCHEMA, InvalidPasswordError


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


class UserInput(PasswordInput):
    """
    Represents the input data for a user.

    Attributes:
        name (str): The name of the user.
        password (str): The password for the user.
    """

    name: str
    username: str

    @validator("username")
    def validate_username(cls, username: str) -> str:
        """
        Validate the username.

        Args:
            username (str): The username to validate.

        Returns:
            str: The validated username.

        Raises:
            ValueError: If the username is empty.
        """
        # Add your validation logic here
        return username


class User(AbstractModel):
    """
    Represents the output data for a user.

    Attributes:
        id (UUID): The unique identifier of the user.
        name (str): The name of the user.
        created (datetime): The datetime when the user was created.
        updated (datetime): The datetime when the user was last updated.
    """

    name: str
    username: str


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_input: UserInput,
) -> User:
    """
    Create a new user.

    Args:
        user (UserInput): The input data for creating the user.

    Returns:
        User: The created user.

    Raises:
        HTTPException: If there is a conflict, bad request, or internal server error.
    """
    try:
        logger.info(f"Creating user with username: {user_input.username}")
        user = UserService().create(
            name=user_input.name,
            username=user_input.username,
            password=user_input.password,
        )
    except ConflictError as exc:
        logger.error(f"Failed to create user: {exc.message}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    except ClientError as exc:
        logger.error(f"Failed to create user: {exc.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    except ServerError as exc:
        logger.error(f"Failed to create user: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    logger.info(f"User created: {user.username}")

    return User(
        id=user.id,
        name=user.name,
        username=user.username,
        created=user.created,
        updated=user.updated,
    )
