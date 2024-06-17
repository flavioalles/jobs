from uuid import UUID

from pydantic import BaseModel

from .base import AbstractModel
from ..utils.application import ApplicationState


class ApplicationInput(BaseModel):
    """
    Represents the input data for an Application.

    Attributes:
        job_id (UUID): The unique identifier of the job associated with the application.
    """

    job_id: UUID


class Application(AbstractModel, ApplicationInput):
    """
    Represents the output data for an application.

    Attributes:
        state (ApplicationState): The state of the job.
        user_id (UUID): The unique identifier of the user associated with the application.
    """

    state: ApplicationState
    user_id: UUID
