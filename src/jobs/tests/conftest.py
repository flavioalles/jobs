import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models.base import Base
from ..models.database import engine, Session


# TODO: Move to app. config.
# engine = create_engine("mysql+pymysql://root:a-password@localhost:3306/test_jobs")
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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


# @pytest.fixture(scope="function")
# def database_session(database_engine):
#     """Provide a transactional scope around a series of operations."""
#     session = Session()
#
#     yield session
#     import ipdb; ipdb.set_trace()
#
#     session.rollback()


@pytest.fixture(scope="function", autouse=True)
def database_setup_and_teardown(database_engine):
    """Clean the database before and after each test."""
    session = Session()
    yield
    # Drop all data after each test
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


# @pytest.fixture(scope="function")
# def database_session(database_engine):
#     """Provide a transactional scope around a series of operations."""
#     return Session()
