from dataclasses import dataclass

from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    InvalidRequestError,
    OperationalError,
    NoResultFound,
)
from .auth import AuthService
from .base import BaseService
from .exceptions import ClientError, ConflictError, ServerError
from ..models.user import User
from ..utils.password import InvalidPasswordError
from ..utils.user import InvalidUsernameError


@dataclass
class UserService(BaseService, AuthService):
    """
    A class that provides methods for creating, updating, getting, deleting and authenticating users.
    """

    def create(self, username: str, name: str, password: str) -> User:
        """
        Creates a new user.

        Parameters:
            name (str): The name of the user.
            password (str): The password for the user.

        Returns:
            User: The newly created user.

        Raises:
            ClientError: If there is a data error or an invalid password is provided.
            ConflictError: If there is a conflict error.
            ServerError: If there is an invalid request or operational error.
        """
        try:
            user = User(username=username, name=name, password=password)
            self.session.add(user)
            self.session.flush()
            self.session.commit()
        except (DataError, InvalidPasswordError, InvalidUsernameError) as exc:
            self.session.rollback()
            raise ClientError(message=str(exc))
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError(message=str(exc))
        except (InvalidRequestError, OperationalError) as exc:
            self.session.rollback()
            raise ServerError(message=str(exc))

        return user

    def update(self):
        """
        Updates an existing user.

        Parameters:
            self: The instance of the UserService class.

        Returns:
            None
        """
        pass

    def get(self):
        """
        Retrieves information about an user.

        Parameters:
            self: The instance of the UserService class.

        Returns:
            None
        """
        pass

    def delete(self):
        """
        Deletes the user.

        Parameters:
            self: The instance of the UserService class.

        Returns:
            None
        """
        pass

    def authenticate(self):
        """
        Authenticates the user.

        Parameters:
            self: The instance of the UserService class.

        Returns:
            None
        """
        pass
