from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column, Unicode

from .base import Base
from ..utils.password import PASSWORD_SCHEMA, InvalidPasswordError


class Credential(Base):
    """
    Abstract model representing a credential.

    Attributes:
        _password (Unicode): The hashed password for the credential.
    """

    __abstract__ = True

    _password = Column("password", Unicode(128), nullable=False)

    @property
    def password(self) -> None:
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str) -> None:
        """
        Setter method for the password attribute.

        Args:
            password (str): The password to be set.

        Raises:
            InvalidPasswordError: If the password does not meet the requirements.

        Returns:
            None
        """
        if not PASSWORD_SCHEMA.validate(password):
            raise InvalidPasswordError()

        self._password = pbkdf2_sha256.hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return pbkdf2_sha256.verify(password, self._password)
