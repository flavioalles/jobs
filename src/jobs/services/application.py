from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    InvalidRequestError,
    OperationalError,
    NoResultFound,
)
from .base import BaseService
from .exceptions import ClientError, ServerError, NotFoundError
from ..models.application import Application
from ..models.job import Job
from ..models.user import User


@dataclass
class ApplicationService(BaseService):
    """
    A class that provides methods for creating, updating, getting, and deleting applications.
    """

    def create(
        self,
        job_id: UUID,
        user_id: UUID,
    ) -> Application:
        """
        Creates a new Application.

        Parameters:
            job_id (UUID): The ID of the job the application is for.
            user_id (UUID): The ID of the user who is applying for the job.

        Returns:
            Application: The newly created application.

        Raises:
            NotFoundError: If the job or user with the given ID is not found.
            ClientError: If there is a data error or an invalid password is provided.
            ServerError: If there is an invalid request or operational error.
        """
        try:
            job = self.session.query(Job).filter_by(id=job_id).one()
        except NoResultFound:
            raise NotFoundError(message=f"Job {job_id} not found.")

        try:
            user = self.session.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            raise NotFoundError(message=f"User {user_id} not found.")

        try:
            application = Application(
                job=job,
                user=user,
            )
            self.session.add(application)
            self.session.flush()
            self.session.commit()
        except (DataError, IntegrityError) as exc:
            self.session.rollback()
            raise ClientError(message=str(exc))
        except (InvalidRequestError, OperationalError) as exc:
            self.session.rollback()
            raise ServerError(message=str(exc))

        return application

    def update(self):
        """
        Updates an existing application.

        Parameters:
            self: The instance of the ApplicationService class.

        Raises:
            NotImplementedError: method is yet to be implemented.

        Returns:
            None
        """
        raise NotImplementedError("ApplicationService.update not implemented.")

    def get(self):
        """
        Retrieves information about an application.

        Parameters:
            self: The instance of the ApplicationService class.

        Raises:
            NotImplementedError: method is yet to be implemented.

        Returns:
            None
        """
        raise NotImplementedError("ApplicationService.get not implemented.")

    def delete(self):
        """
        Deletes the application.

        Parameters:
            self: The instance of the ApplicationService class.

        Raises:
            NotImplementedError: method is yet to be implemented.

        Returns:
            None
        """
        raise NotImplementedError("ApplicationService.delete not implemented.")
