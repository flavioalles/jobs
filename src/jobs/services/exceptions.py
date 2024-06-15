from dataclasses import dataclass


@dataclass
class BaseError(Exception):
    """
    Base exception class for all exceptions in the application.
    """

    message: str


@dataclass
class ServerError(BaseError):
    """
    Exception raised when an error occurs on the server.
    """

    pass


@dataclass
class ClientError(BaseError):
    """
    Exception raised when an error occurs on the client side.
    """

    pass
