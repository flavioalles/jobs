from sqlalchemy import Column, UUID, Unicode, UnicodeText, Enum, Numeric, ForeignKey
from sqlalchemy.orm import relationship, validates

from .base import Abstract
from ..utils.job import JobContract, JobMode, JobState, InvalidSalaryError


class Job(Abstract):
    """
    Represents a job entity.

    Attributes:
        title (str): The title of the job.
        description (str): The description of the job.
        state (JobState): The state of the job.
        salary (float): The salary of the job.
        mode (JobMode): The mode of the job.
        contract (JobContract): The contract type of the job.
        organization_id (int): The ID of the organization associated with the job.
        organization (Organization): The organization associated with the job.
    """

    __tablename__ = "jobs"

    title = Column(Unicode(255), nullable=False, index=True)
    description = Column(UnicodeText)
    state = Column(Enum(JobState), nullable=False, index=True, default=JobState.DRAFT)
    salary = Column(Numeric(10, 2), nullable=False, index=True)
    mode = Column(Enum(JobMode), nullable=False, index=True)
    contract = Column(Enum(JobContract), nullable=False, index=True)
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )
    organization = relationship("Organization", back_populates="jobs")

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title})>"

    @validates("salary")
    def validate_salary(self, key, salary):
        """
        Validates the salary value.

        Args:
            key (str): The key associated with the salary value.
            salary (float): The salary value to be validated.

        Returns:
            float: The validated salary value.

        Raises:
            InvalidSalaryError: If the salary value is less than or equal to 0.
        """
        try:
            if salary <= 0:
                raise InvalidSalaryError(salary=salary)
        except TypeError:
            raise InvalidSalaryError(salary=salary)

        return salary
