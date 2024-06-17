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
from ..models.credential import InvalidPasswordError
from ..models.database import Session
from ..models.organization import Organization


@dataclass
class OrganizationService(BaseService, AuthService):
    """
    A class that provides methods for creating, updating, getting, deleting and authenticating organizations.
    """

    def create(self, name: str, password: str) -> Organization:
        """
        Creates a new organization.

        Parameters:
            name (str): The name of the organization.
            password (str): The password for the organization.

        Returns:
            Organization: The newly created organization.

        Raises:
            ClientError: If there is a data error or an invalid password is provided.
            ConflictError: If there is a conflict error.
            ServerError: If there is an invalid request or operational error.
        """
        try:
            organization = Organization(name=name, password=password)
            self.session.add(organization)
            self.session.flush()
            self.session.commit()
        except (DataError, InvalidPasswordError) as exc:
            self.session.rollback()
            raise ClientError(message=str(exc))
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError(message=str(exc))
        except (InvalidRequestError, OperationalError) as exc:
            self.session.rollback()
            raise ServerError(message=str(exc))

        return organization

    def update(self):
        """
        Updates an existing organization.

        Parameters:
            self: The instance of the OrganizationService class.

        Returns:
            None
        """
        pass

    def get(self, id: str | None = None, name: str | None = None) -> Organization:
        """
        Retrieves information about an organization.

        Parameters:
            id (str | None): The ID of the organization to retrieve information for.
            name (str | None): The name of the organization to retrieve information for.

        Returns:
            Organization: An instance of the Organization class representing the retrieved organization.

        Raises:
            ClientError: If neither id nor name is provided, or if both id and name are provided.
            NotFoundError: If the organization with the specified id or name is not found.
        """
        if id is None and name is None:
            raise ClientError(message="Either id or name must be provided.")
        elif id is not None and name is not None:
            raise ClientError(
                message="Both id and name cannot be provided simultaneously."
            )

        try:
            return (
                self.session.query(Organization).filter_by(id=id).one()
                if id is not None
                else self.session.query(Organization).filter_by(name=name).one()
            )
        except NoResultFound:
            raise NotFoundError(message=f"Organization {id or name} not found.")

    def delete(self):
        """
        Deletes the organization.

        Parameters:
            self: The instance of the OrganizationService class.

        Returns:
            None
        """
        pass

    def authenticate(self, name: str, password: str) -> Organization:
        """
        Authenticates an organization.

        Parameters:
            name (str): The name of the organization to authenticate.
            password (str): The password for the organization.

        Returns:
            Organization: The authenticated organization.

        Raises:
            NotFoundError: If the organization with the given name is not found.
            InvalidPasswordError: If the password is invalid.
        """
        try:
            organization = self.session.query(Organization).filter_by(name=name).one()
        except NoResultFound:
            raise NotFoundError(message=f"Organization {name} not found.")

        if not organization.check_password(password):
            raise InvalidPasswordError(message="Invalid password.")

        return organization
