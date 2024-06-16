import pytest

from ...models.organization import Organization


class TestOrganizationService:

    def test_when_create_is_successful(self, organization_service, valid_password):
        assert organization_service.session.query(Organization).count() == 0

        organization_service.create(name="an-organization", password=valid_password)

        assert organization_service.session.query(Organization).count() == 1

        an_organization = organization_service.session.query(Organization).one()
        assert an_organization.name == "an-organization"
        assert an_organization.check_password(valid_password) is True
