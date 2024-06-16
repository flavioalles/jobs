import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.sql import func

Base = declarative_base()


class Abstract(Base):
    """
    Base class for defining abstract models.

    This class should be inherited by other models to provide common attributes and operations.

    Attributes:
        __abstract__ (bool): Indicates whether the class is abstract or not.

    """

    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    created = Column(
        DateTime(timezone=True), default=func.utc_timestamp(), nullable=False
    )
    updated = Column(
        DateTime(timezone=True),
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
        nullable=False,
    )
