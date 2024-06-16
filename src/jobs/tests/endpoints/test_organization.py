import json
import pytest

from ...models.organization import Organization


class TestOrganizationEndpoints:

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
