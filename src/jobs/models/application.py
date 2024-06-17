from sqlalchemy import Column, UUID, Enum, ForeignKey
from sqlalchemy.orm import relationship

from .base import Abstract
from ..utils.application import ApplicationState


class Application(Abstract):
    """
    Represents an application entity.

    Attributes:
        state (ApplicationState): The state of the job.
        job_id (UUID): The ID of the job associated with the application..
        job (Job): The job associated with the application.
        user_id (UUID): The ID of the user associated with the application.
        user (User): The user associated with the application.
    """

    __tablename__ = "applications"

    state = Column(
        Enum(ApplicationState),
        nullable=False,
        index=True,
        default=ApplicationState.DRAFT,
    )
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    job = relationship("Job", back_populates="applications")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="applications")

    def __repr__(self):
        return f"<Application(id={self.id})>"
