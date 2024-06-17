from enum import Enum


class ApplicationState(Enum):
    """
    Represents the state of an application - to be used at Application.state.

    Attributes:
        DRAFT (str): The application is in draft state.
        SUBMITTED (str): The application has been submitted.
        ACCEPTED (str): The application has been accepted.
        REJECTED (str): The application has been rejected.
    """

    DRAFT: str = "DRAFT"
    SUBMITTED: str = "SUBMITTED"
    ACCEPTED: str = "ACCEPTED"
    REJECTED: str = "REJECTED"
