import pytest

from ...models.organization import Organization


class TestCreateOrganizationService:

    def test_when_create_is_successful(self, organization_service, valid_password):
        assert organization_service.session.query(Organization).count() == 0

        organization_service.create(name="an-organization", password=valid_password)

        assert organization_service.session.query(Organization).count() == 1

        an_organization = organization_service.session.query(Organization).one()
        assert an_organization.name == "an-organization"
        assert an_organization.check_password(valid_password) is True


class TestGetOrganizationService:

    def test_when_get_by_id_is_successful(self, organization_service, valid_password):
        organization_service.create(name="an-organization", password=valid_password)

        id = organization_service.session.query(Organization).one().id

        an_organization = organization_service.get(id=id)

        assert an_organization.name == "an-organization"
        assert an_organization.check_password(valid_password) is True

    def test_when_get_by_name_is_successful(self, organization_service, valid_password):
        organization_service.create(name="an-organization", password=valid_password)

        an_organization = organization_service.get(name="an-organization")

        assert an_organization.name == "an-organization"
        assert an_organization.check_password(valid_password) is True


class TestAuthenticateOrganizationService:

    def test_when_authenticate_is_successful(
        self, organization_service, valid_password
    ):
        organization_service.create(name="an-organization", password=valid_password)

        an_organization = organization_service.authenticate(
            name="an-organization", password=valid_password
        )

        assert an_organization.name == "an-organization"
        assert an_organization.check_password(valid_password) is True
