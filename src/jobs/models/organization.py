from sqlalchemy import Column, Unicode
from sqlalchemy.orm import relationship

from .base import Abstract
from .credential import Credential
from .job import Job


class Organization(Abstract, Credential):
    """
    Model representing an organization.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (Unicode): The name of the organization.
        jobs (relationship): The relationship to the jobs associated with the organization.
    """

    __tablename__ = "organizations"

    name = Column(Unicode(255), nullable=False, unique=True)
    jobs = relationship(Job, back_populates="organization")

    def __repr__(self):
        return f"<Organization(name={self.name})>"
