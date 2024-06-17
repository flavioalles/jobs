import logging
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import validator

from .application import Application, ApplicationInput
from .base import AbstractModel, PasswordInput, Token
from ..services.application import ApplicationService
from ..services.exceptions import ClientError, ConflictError, NotFoundError, ServerError
from ..services.user import UserService
from ..utils.auth import (
    create_jwt_token,
    get_jwt_subject,
    FailedJWTDecodeError,
    NoJWTSubjectError,
)
from ..utils.password import PASSWORD_SCHEMA, InvalidPasswordError


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth")


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


@router.post("/auth", status_code=status.HTTP_200_OK)
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Authenticate a user.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends()]): The form data containing the username and password.

    Returns:
        Token: The token for the authenticated user.

    Raises:
        HTTPException: If there is a failure to authenticate.
    """
    try:
        logger.info(f"Authenticating user {form_data.username}.")
        user = UserService().authenticate(
            username=form_data.username, password=form_data.password
        )
    except (NotFoundError, InvalidPasswordError) as exc:
        logger.error(f"Failed to authenticate user: {exc.message}")
        # NOTE: not a good practice to return detailed error messages in this use case.
        # Hence, avoiding returning the actual error message.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failure to authenticate."
        )

    logger.info(f"Authenticated user {form_data.username}.")

    return Token(access_token=create_jwt_token(user.username))


async def get_authenticated_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Retrieves the authenticated user based on the provided token.

    Args:
        token (str): The authentication token.

    Returns:
        User: The authenticated User.

    Raises:
        HTTPException: If the token is invalid or the user cannot be retrieved.
    """
    try:
        user = UserService().get(username=get_jwt_subject(token))
    except (FailedJWTDecodeError, NoJWTSubjectError, NotFoundError) as exc:
        logger.error(f"Failed to decode JWT token/get user: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return User(
        id=user.id,
        name=user.name,
        username=user.username,
        created=user.created,
        updated=user.updated,
    )


@router.post("/{user_id}/applications", status_code=status.HTTP_201_CREATED)
async def create_application(
    user_id: UUID,
    application_input: ApplicationInput,
    authenticated_user: Annotated[User, Depends(get_authenticated_user)],
) -> Application:
    """
    Create an application for a job.

    Args:
        user_id (UUID): The ID of the user creating the application.
        application_input (ApplicationInput): The input data for creating the application.
        authenticated_user (User): The authenticated user.

    Returns:
        Application: The created application.

    Raises:
        HTTPException: If there is an error creating the application.

    """
    if user_id != authenticated_user.id:
        logger.error(
            f"Failed to create application: User mismatch (path: {user_id}, authenticated: {authenticate_id.id})."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Failed to create application: User mismatch.",
        )

    try:
        logger.info(
            f"Creating application for job: {application_input.job_id} (user: {user_id})."
        )
        application = ApplicationService().create(
            job_id=application_input.job_id,
            user_id=user_id,
        )
    except NotFoundError as exc:
        logger.error(f"Failed to create application: {exc.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except ClientError as exc:
        logger.error(f"Failed to create application: {exc.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    except ServerError as exc:
        logger.error(f"Failed to create application: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    logger.info(
        f"Application created for job: {application_input.job_id} (user: {user_id})."
    )

    return Application(
        id=application.id,
        state=application.state,
        job_id=application.job_id,
        user_id=application.user_id,
        created=application.created,
        updated=application.updated,
    )


@router.get("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_users() -> None:
    """
    Retrieve users.

    Args:
        None

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.get("/{user_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_user(user_id: UUID) -> None:
    """
    Retrieve a user.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.patch("/{user_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def patch_user(user_id: UUID) -> None:
    """
    Update a user.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.delete("/{user_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def delete_user(user_id: UUID) -> None:
    """
    Delete a user.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )


@router.get("/{user_id}/applications", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_applications_by_user(user_id: UUID) -> None:
    """
    Retrieve applications for a user.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        None

    Raises:
        HTTPException: Operation not implemented yet.
    """
    logger.warning("Yet to be implemented.")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Yet to be implemented."
    )
