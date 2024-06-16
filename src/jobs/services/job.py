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
from ..models.job import Job
from ..models.organization import Organization
from ..utils.job import JobMode, JobContract


@dataclass
class JobService(BaseService):
    """
    A class that provides methods for creating, updating, getting, and deleting jobs.
    """

    def create(
        self,
        organization_id: UUID,
        title: str,
        salary: float,
        mode: JobMode,
        contract: JobContract,
        description: str | None = None,
    ) -> Job:
        """
        Creates a new job.

        Parameters:
            organization_id (UUID): The ID of the organization the job belongs to.
            title (str): The title of the job.
            salary (float): The salary of the job.
            mode (JobMode): The mode of the job.
            contract (JobContract): The contract type of the job.
            description (str, optional): The description of the job. Defaults to None.

        Returns:
            Job: The newly created job.

        Raises:
            NotFoundError: If the organization with the given ID is not found.
            ClientError: If there is a data error or an invalid password is provided.
            ServerError: If there is an invalid request or operational error.
        """
        try:
            organization = (
                self.session.query(Organization).filter_by(id=organization_id).one()
            )
        except NoResultFound:
            raise NotFoundError(message=f"Organization {organization_id} not found.")

        try:
            job = Job(
                title=title,
                salary=salary,
                mode=mode,
                contract=contract,
                description=description,
                organization=organization,
            )
            self.session.add(job)
            self.session.flush()
            self.session.commit()
        except (DataError, IntegrityError) as exc:
            self.session.rollback()
            raise ClientError(message=str(exc))
        except (InvalidRequestError, OperationalError) as exc:
            self.session.rollback()
            raise ServerError(message=str(exc))

        return job

    def update(self):
        """
        Updates an existing job.

        Parameters:
            self: The instance of the JobService class.

        Returns:
            None
        """
        pass

    def get(self):
        """
        Retrieves information about an job.

        Parameters:
            self: The instance of the JobService class.

        Returns:
            None
        """
        pass

    def delete(self):
        """
        Deletes the job.

        Parameters:
            self: The instance of the JobService class.

        Returns:
            None
        """
        pass
