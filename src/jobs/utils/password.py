"""
This module defines a password schema using the `password_validator` library.

The `password_schema` variable represents the password validation rules.
It requires a password to be at least 16 characters long, contain at least one
uppercase letter, one lowercase letter, one digit, and one special character.

Example usage:
    password = "MySecurePassword123!"
    is_valid = password_schema.validate(password)
    if is_valid:
        print("Password is valid.")
    else:
        print("Password is invalid.")
"""

from password_validator import PasswordValidator


PASSWORD_SCHEMA = (
    PasswordValidator()
    .min(16)
    .has()
    .uppercase()
    .has()
    .lowercase()
    .has()
    .digits()
    .has(
        r'[!@#\$%\^&\*\(\)_\+\[\]{};\'\\:"|<,>\./\?`~-]'
    )  # NOTE: This checks for special characters
)


class InvalidPasswordError(Exception):
    """Raised when an invalid password is provided."""

    def __init__(self) -> None:
        super().__init__("Invalid password.")
