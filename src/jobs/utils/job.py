from enum import Enum


class InvalidSalaryError(Exception):
    """
    Exception raised when an invalid salary is provided.

    Attributes:
        salary (float): The invalid salary.
    """

    def __init__(self, salary: float) -> None:
        super().__init__(f"Invalid salary (must be a positive number): {salary}.")


class JobState(Enum):
    """
    Represents the state of a job - used at Job.state.

    Attributes:
        DRAFT (str): The job is in draft mode - i.e. not (yet) open for applications.
        OPEN (str): The job is open - i.e. open for applications.
        CLOSED (str): The job is closed - i.e. closed for applications.
        CANCELLED (str): The job is cancelled - i.e. finished without hiring anyone.
        DONE (str): The job is done - i.e. finished hiring someone.
    """

    DRAFT: str = "DRAFT"
    OPEN: str = "OPEN"
    CLOSED: str = "CLOSED"
    CANCELLED: str = "CANCELLED"
    DONE: str = "DONE"


class JobMode(Enum):
    """
    Enumeration class representing the different modes of a job -
    to be used at Jobs.mode.

    Attributes:
        HYBRID: Indicates a hybrid job.
        ON_SITE: Indicates an on-site job.
        REMOTE: Indicates a remote job.
    """

    HYBRID: str = "HYBRID"
    ON_SITE: str = "ON_SITE"
    REMOTE: str = "REMOTE"


class JobContract(Enum):
    """
    Enumeration class representing the different contract options of a job -
    to be used at Jobs.contract.

    Attributes:
        FULL_TIME: Indicates a full-time job.
        PART_TIME: Indicates a part-time job.
        TEMPORARY: Indicates a temporary job.
    """

    FULL_TIME: str = "FULL_TIME"
    PART_TIME: str = "PART_TIME"
    TEMPORARY: str = "TEMPORARY"
