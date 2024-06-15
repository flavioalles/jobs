import pytest

from ...models.organization import Organization
from ...services.organization import OrganizationService


@pytest.fixture(scope="function")
def organization_service():
    service = OrganizationService()
    yield service
    service.session.rollback()


class TestOrganizationService:

    def test_when_create_is_successful(self, organization_service):
        assert organization_service.session.query(Organization).count() == 0

        organization_service.create(name="an-organization")

        assert organization_service.session.query(Organization).count() == 1
        assert (
            organization_service.session.query(Organization).one().name
            == "an-organization"
        )
