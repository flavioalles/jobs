import pytest

from ...models.organization import Organization


class TestOrganizationService:

    def test_when_create_is_successful(self, organization_service):
        assert organization_service.session.query(Organization).count() == 0

        organization_service.create(name="an-organization")

        assert organization_service.session.query(Organization).count() == 1
        assert (
            organization_service.session.query(Organization).one().name
            == "an-organization"
        )
