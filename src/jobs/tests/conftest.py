import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models.base import Base
from ..models.database import Session
from ..services.application import ApplicationService
from ..services.job import JobService
from ..services.organization import OrganizationService
from ..services.user import UserService
from ..settings.base import Settings


engine = create_engine(Settings().database_url)


@pytest.fixture(scope="session")
def database_engine():
    """
    Returns the SQLAlchemy engine object.

    :return: SQLAlchemy engine object.
    """
    return engine


@pytest.fixture(scope="session", autouse=True)
def database_setup(database_engine):
    """Create all tables before the test session and drop them after."""
    Base.metadata.create_all(bind=database_engine)
    yield
    Base.metadata.drop_all(bind=database_engine)


@pytest.fixture(scope="function", autouse=True)
def database_setup_and_teardown(database_engine):
    """Clean the database before and after each test."""
    session = Session()
    yield
    # Drop all data after each test
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture(scope="function")
def organization_service():
    service = OrganizationService()
    yield service
    service.session.rollback()


@pytest.fixture(scope="session")
def valid_password():
    return "jqM.[+D;]TK*&q*jHG<JC]yAu1Evtv6K"


@pytest.fixture(scope="function")
def job_service():
    service = JobService()
    yield service
    service.session.rollback()


@pytest.fixture(scope="function")
def user_service():
    service = UserService()
    yield service
    service.session.rollback()


@pytest.fixture(scope="function")
def application_service():
    service = ApplicationService()
    yield service
    service.session.rollback()
