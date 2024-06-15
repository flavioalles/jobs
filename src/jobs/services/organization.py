from dataclasses import dataclass

from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    InvalidRequestError,
    OperationalError,
)
from .base import BaseService
from .exceptions import ClientError, ConflictError, ServerError
from ..models.database import Session
from ..models.organization import Organization


@dataclass
class OrganizationService(BaseService):
    """
    A class that provides methods for creating, updating, getting, and deleting organizations.
    """

    def create(self, name: str) -> Organization:
        """
        Creates a new organization.

        Parameters:
            self: The instance of the OrganizationService class.
            name (str): The name of the organization.

        Returns:
            Organization: The newly created organization.

        Raises:
            ClientError: If there is a data or integrity error.
            ServerError: If there is an invalid request or operational error.
        """
        organization = Organization(name=name)
        try:
            self.session.add(organization)
            self.session.flush()
            self.session.commit()
        except DataError as exc:
            self.session.rollback()
            raise ClientError(message=str(exc))
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError(message=str(exc))
        except (InvalidRequestError, OperationalError):
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

    def get(self):
        """
        Retrieves information about an organization.

        Parameters:
            self: The instance of the OrganizationService class.

        Returns:
            None
        """
        pass

    def delete(self):
        """
        Deletes the organization.

        Parameters:
            self: The instance of the OrganizationService class.

        Returns:
            None
        """
        pass
