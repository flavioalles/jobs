from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator

from ..utils.password import PASSWORD_SCHEMA, InvalidPasswordError


class AbstractModel(BaseModel):
    """
    Represents the output data for an organization.

    Attributes:
        id (UUID): The unique identifier of the organization.
        created (datetime): The datetime when the organization was created.
        updated (datetime): The datetime when the organization was last updated.
    """

    id: UUID
    created: datetime
    updated: datetime


class PasswordInput(BaseModel):
    """
    Represents the input data for an organization.

    Attributes:
        password (str): The password for the organization.
    """

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
            InvalidPasswordError: If the password is invalid.
        """
        if not PASSWORD_SCHEMA.validate(password):
            raise InvalidPasswordError()

        return password


class Token(BaseModel):
    """
    Represents the output data for an authentication operation.

    Attributes:
        access_token (str): The access token.
        token_type (str): The token type.
    """

    access_token: str
    token_type: str = "bearer"
