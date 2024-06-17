from email_validator import validate_email, EmailNotValidError
from sqlalchemy import Column, Unicode
from sqlalchemy.orm import relationship, validates

from .base import Abstract
from .credential import Credential
from ..utils.user import InvalidUsernameError


class User(Abstract, Credential):
    """
    Model representing a user.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (Unicode): The name of the user.
        username (Unicode): The username of the user. Has to be an email.
    """

    __tablename__ = "users"

    name = Column(Unicode(255), nullable=False)
    username = Column(Unicode(255), nullable=False, unique=True, index=True)
    applications = relationship("Application", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

    @validates("username")
    def validate_username(self, key, username):
        """
        Validates the given username - which should be an email.

        Parameters:
        - key (str): The key associated with the username.
        - username (str): The username to be validated.

        Returns:
        - str: The normalized email address.

        Raises:
        - InvalidUsername: If the username is not a valid email address.
        """
        try:
            email = validate_email(username)
        except EmailNotValidError:
            raise InvalidUsernameError(
                f"Invalid username (i.e. email address): {username}."
            )

        return email.normalized
