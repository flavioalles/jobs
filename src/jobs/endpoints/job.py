from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .base import AbstractModel
from ..utils.job import JobMode, JobContract, JobState


class JobInput(BaseModel):
    """
    Represents the input data for a job.

    Attributes:
        title (str): The title of the job.
        salary (float): The salary for the job.
        mode (JobMode): The mode of the job.
        contract (JobContract): The contract type for the job.
        description (str, optional): The description of the job. Defaults to None.
    """

    title: str
    salary: float
    mode: JobMode
    contract: JobContract
    description: str | None = None


class Job(AbstractModel, JobInput):
    """
    Represents the output data for a job.

    Attributes:
        state (JobState): The state of the job.
        organization_id (UUID): The unique identifier of the organization associated with the job.
    """

    state: JobState
    organization_id: UUID
