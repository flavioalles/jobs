from sqlalchemy import Column, Unicode

from .base import Abstract
from .credential import Credential


class Organization(Abstract, Credential):
    """
    Model representing an organization.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (Unicode): The name of the organization.
    """

    __tablename__ = "organizations"

    name = Column(Unicode(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<Organization(name={self.name})>"
