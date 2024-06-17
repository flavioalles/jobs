import json
import pytest

from ...models.application import Application
from ...models.job import Job
from ...models.organization import Organization
from ...models.user import User
from ...utils.application import ApplicationState
from ...utils.auth import create_jwt_token
from ...utils.job import JobContract, JobMode


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


class TestCreateApplicationEndpoint:
    """
    Test class for the create job endpoint.
    """

    auth: str = "/api/v1/users/auth"
    resource: str = "/api/v1/users/{user_id}/applications"

    @classmethod
    def _authenticate(cls, test_app, username, password):
        """
        Authenticate a user.

        This method authenticates a user by sending a POST request to the authentication endpoint with the provided
        username and password. It returns the access token obtained from the response.

        Args:
            test_app (TestClient): The test client used to make HTTP requests.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: The access token.
        """
        return test_app.post(
            cls.auth,
            data={"username": username, "password": password},
        ).json()["access_token"]

    def test_when_create_job_is_successful(
        self, test_app, application_service, valid_password
    ):
        """
        Test case for creating an application successfully.

        Args:
            test_app (TestClient): The test client for the application.
            job_service (JobService): The job service.
            valid_password (str): A valid password for the organization.

        Returns:
            None
        """
        application_service.session.add(
            Organization(name="an-organization", password=valid_password)
        )
        an_organization = application_service.session.query(Organization).one()
        application_service.session.add(
            Job(
                title="a-job",
                salary=float(100000),
                mode=JobMode.ON_SITE,
                contract=JobContract.FULL_TIME,
                organization=an_organization,
            )
        )
        application_service.session.add(
            User(name="a-user", username="username@server.io", password=valid_password)
        )
        application_service.session.flush()
        a_job = application_service.session.query(Job).one()
        a_user = application_service.session.query(User).one()

        response = test_app.post(
            self.resource.format(user_id=a_user.id),
            data=json.dumps({"job_id": str(a_job.id)}),
            headers={
                "Authorization": f"Bearer {self._authenticate(test_app, "username@server.io", valid_password)}"
            },
        )

        assert application_service.session.query(Application).count() == 1

        an_application = application_service.session.query(Application).one()

        assert response.status_code == 201
        assert response.json()["id"] == str(an_application.id)
        assert response.json()["state"] == ApplicationState.DRAFT.value
        assert response.json()["job_id"] == str(a_job.id)
        assert response.json()["user_id"] == str(a_user.id)
        assert response.json()["created"] == an_application.created.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        assert response.json()["updated"] == an_application.updated.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
