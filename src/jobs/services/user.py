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
from .exceptions import ClientError, ConflictError, ServerError, NotFoundError
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

        Raises:
            NotImplementedError: method is yet to implemented.

        Returns:
            None
        """
        raise NotImplementedError("UserService.update is not implemented.")

    def get(self, id: str | None = None, username: str | None = None) -> User:
        """
        Retrieve a user by their ID or username.

        Args:
            id (str, optional): The ID of the user. Defaults to None.
            username (str, optional): The username of the user. Defaults to None.

        Returns:
            User: The user object.

        Raises:
            ClientError: If neither id nor username is provided, or if both id and username are provided.
            NotFoundError: If the user is not found.
        """

        if id is None and username is None:
            raise ClientError(message="Either id or name must be provided.")
        elif id is not None and username is not None:
            raise ClientError(
                message="Both id and name cannot be provided simultaneously."
            )

        try:
            return (
                self.session.query(User).filter_by(id=id).one()
                if id is not None
                else self.session.query(User).filter_by(username=username).one()
            )
        except NoResultFound:
            raise NotFoundError(message=f"User {id or name} not found.")

    def delete(self):
        """
        Deletes the user.

        Parameters:
            self: The instance of the UserService class.

        Raises:
            NotImplementedError: Method is yet to be implemented.

        Returns:
            None
        """
        raise NotImplementedError("UserService.delete is not implemented.")

    def authenticate(self, username: str, password: str) -> User:
        """
        Authenticates a user.

        Parameters:
            username (str): The username of the user to authenticate.
            password (str): The password for the user.

        Returns:
            User: The authenticated user.

        Raises:
            NotFoundError: If the user with the given name is not found.
            InvalidPasswordError: If the password is invalid.
        """
        try:
            user = self.session.query(User).filter_by(username=username).one()
        except NoResultFound:
            raise NotFoundError(message=f"User {username} not found.")

        if not user.check_password(password):
            raise InvalidPasswordError(message="Invalid password.")

        return user
