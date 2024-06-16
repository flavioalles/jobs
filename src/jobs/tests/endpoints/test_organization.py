import json
import pytest

from ...models.job import Job
from ...models.organization import Organization
from ...utils.job import JobContract, JobMode, JobState


class TestCreateOrganizationEndpoint:
    """
    Test class for the create organization endpoint.
    """

    resource: str = "/api/v1/organizations"

    def test_when_create_organization_is_successful(
        self, test_app, organization_service, valid_password
    ):
        """
        Test case for creating an organization successfully.

        Args:
            test_app: The test client for the application.
            organization_service: The organization service.

        Returns:
            None
        """
        assert organization_service.session.query(Organization).count() == 0

        response = test_app.post(
            self.resource,
            data=json.dumps({"name": "an-organization", "password": valid_password}),
        )

        assert organization_service.session.query(Organization).count() == 1

        an_organization = organization_service.session.query(Organization).one()

        assert response.status_code == 201
        assert response.json()["name"] == "an-organization"
        assert response.json()["id"] == str(an_organization.id)
        assert response.json()["created"] == an_organization.created.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        assert response.json()["updated"] == an_organization.updated.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )


class TestCreateJobEndpoint:
    """
    Test class for the create job endpoint.
    """

    resource: str = "/api/v1/organizations/{organization_id}/jobs"

    def test_when_create_job_is_successful(self, test_app, job_service, valid_password):
        """
        Test case for creating a job successfully.

        Args:
            test_app (TestClient): The test client for the application.
            job_service (JobService): The job service.
            valid_password (str): A valid password for the organization.

        Returns:
            None
        """
        job_service.session.add(
            Organization(name="an-organization", password=valid_password)
        )
        job_service.session.flush()
        an_organization = job_service.session.query(Organization).one()

        assert job_service.session.query(Job).count() == 0

        response = test_app.post(
            self.resource.format(organization_id=an_organization.id),
            data=json.dumps(
                {
                    "title": "a-job",
                    "salary": float(100000),
                    "mode": JobMode.ON_SITE.value,
                    "contract": JobContract.FULL_TIME.value,
                }
            ),
        )

        assert job_service.session.query(Job).count() == 1

        a_job = job_service.session.query(Job).one()

        assert response.status_code == 201
        assert response.json()["title"] == "a-job"
        assert response.json()["salary"] == float(100000)
        assert response.json()["mode"] == JobMode.ON_SITE.value
        assert response.json()["contract"] == JobContract.FULL_TIME.value
        assert response.json()["description"] == None
        assert response.json()["id"] == str(a_job.id)
        assert response.json()["organization_id"] == str(an_organization.id)
        assert response.json()["state"] == JobState.DRAFT.value
        assert response.json()["created"] == a_job.created.strftime("%Y-%m-%dT%H:%M:%S")
        assert response.json()["updated"] == a_job.updated.strftime("%Y-%m-%dT%H:%M:%S")
