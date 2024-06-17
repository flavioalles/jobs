import json
import pytest

from ...models.user import User
from ...utils.auth import create_jwt_token


class TestCreateUserEndpoint:
    """
    Test class for the create user endpoint.
    """

    resource: str = "/api/v1/users"

    def test_when_create_user_is_successful(
        self, test_app, user_service, valid_password
    ):
        """
        Test case for creating a user successfully.

        Args:
            test_app: The test client for the application.
            user_service: The user service.
            valid_password: A valid password for the user.

        Returns:
            None
        """
        assert user_service.session.query(User).count() == 0

        response = test_app.post(
            self.resource,
            data=json.dumps(
                {
                    "name": "a-user",
                    "username": "username@server.io",
                    "password": valid_password,
                }
            ),
        )

        assert user_service.session.query(User).count() == 1

        a_user = user_service.session.query(User).one()

        assert response.status_code == 201
        assert response.json()["name"] == "a-user"
        assert response.json()["username"] == "username@server.io"
        assert response.json()["id"] == str(a_user.id)
        assert response.json()["created"] == a_user.created.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        assert response.json()["updated"] == a_user.updated.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )


class TestAuthenticateUserEndpoint:
    """
    Test class for the authenticate user endpoint.
    """

    resource: str = "/api/v1/users/auth"

    def test_when_authenticate_user_is_successful(
        self, test_app, user_service, valid_password
    ):
        """
        Test case for authenticating a user successfully.

        Args:
            test_app: The test client for the application.
            user_service: The user service.
            valid_password: A valid password for the user.

        Returns:
            None
        """
        user_service.session.add(
            User(name="a-user", username="username@server.io", password=valid_password)
        )
        user_service.session.flush()

        response = test_app.post(
            self.resource,
            data={"username": "username@server.io", "password": valid_password},
        )

        assert response.status_code == 200
        assert response.json()["access_token"] == create_jwt_token("username@server.io")
        assert response.json()["token_type"] == "bearer"
