from enum import Enum

from transitions import Machine

from .exceptions import InvalidTransitionError


class InvalidSalaryError(Exception):
    """
    Exception raised when an invalid salary is provided.

    Attributes:
        salary (float): The invalid salary.
    """

    def __init__(self, salary: float) -> None:
        super().__init__(f"Invalid salary (must be a positive number): {salary}.")


class InvalidJobStateError(InvalidTransitionError):
    """
    Exception raised when an invalid job state transition is attempted.

    Attributes:
        old (str): The old job state.
        new (str): The new job state.
    """

    def __init__(self, old: str, new: str) -> None:
        super().__init__(old, new)


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


class JobStateMachine:
    """
    Represents a state machine for managing job statees - used to handle transitions at Job.state.

    Attributes:
        states (list[str]): A list of all possible job state values - derived from JobState.
    """

    states: list[str] = [state.value for state in JobState]

    def __init__(self) -> None:
        self.machine: Machine = Machine(
            model=self, states=JobStateMachine.states, initial=JobState.OPEN.value
        )

        self.machine.add_transition(
            trigger="open", source=JobState.DRAFT.value, dest=JobState.OPEN.value
        )
        self.machine.add_transition(
            trigger="close", source=JobState.OPEN.value, dest=JobState.CLOSED.value
        )
        self.machine.add_transition(
            trigger="cancel",
            source=[JobState.OPEN.value, JobState.CLOSED.value],
            dest=JobState.CANCELLED.value,
        )
        self.machine.add_transition(
            trigger="finish",
            source=[JobState.OPEN.value, JobState.CLOSED.value],
            dest=JobState.DONE.value,
        )
        self.machine.add_transition(
            trigger="reopen", source=JobState.CLOSED.value, dest=JobState.OPEN.value
        )


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
