from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import PyJWTError

from ..settings.base import Settings


class NoJWTSubjectError(Exception):
    """
    Exception raised when no subject is found in a JWT token.
    """

    pass


class FailedJWTDecodeError(Exception):
    """
    Exception raised when a JWT token fails to decode.
    """

    pass


def create_jwt_token(subject: str) -> str:
    """
    Create a JWT token with the provided subject.

    Args:
        subject (str): The subject of the token.

    Returns:
        str: The encoded JWT token.
    """
    settings = Settings()

    return jwt.encode(
        {
            "sub": subject,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.jwt_token_expiration_minutes),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_jwt_token(token: str) -> dict:
    """
    Decode a JWT token.

    Args:
        token (str): The token to be decoded.

    Returns:
        dict: The decoded token data.
    """
    settings = Settings()

    return jwt.decode(
        token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
    )


def get_jwt_subject(token: str) -> str:
    """
    Get the subject of a JWT token.

    Args:
        token (str): The JWT token from which to extract the subject.

    Returns:
        str: The subject of the JWT token.

    Raises:
        NoJWTSubjectError: If no subject is found in the token.
        FailedJWTDecodeError: If there is an error decoding the JWT token.
    """
    try:
        subject = decode_jwt_token(token).get("sub")
    except PyJWTError as exc:
        raise FailedJWTDecodeError(f"Failed to decode JWT token: {exc}")

    if subject is None:
        raise NoJWTSubjectError("No subject found in token.")

    return subject
