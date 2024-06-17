import pytest

from ...models.user import User


class TestCreateUserService:

    def test_when_create_is_successful(self, user_service, valid_password):
        assert user_service.session.query(User).count() == 0

        user_service.create(
            name="a-user", username="name@server.io", password=valid_password
        )

        assert user_service.session.query(User).count() == 1

        a_user = user_service.session.query(User).one()
        assert a_user.name == "a-user"
        assert a_user.check_password(valid_password) is True


class TestGetUserService:

    def test_when_get_by_id_is_successful(self, user_service, valid_password):
        user_service.create(
            name="a-user", username="username@server.io", password=valid_password
        )

        id = user_service.session.query(User).one().id

        a_user = user_service.get(id=id)

        assert a_user.name == "a-user"
        assert a_user.username == "username@server.io"
        assert a_user.check_password(valid_password) is True

    def test_when_get_by_name_is_successful(self, user_service, valid_password):
        user_service.create(
            name="a-user", username="username@server.io", password=valid_password
        )

        a_user = user_service.get(username="username@server.io")

        assert a_user.name == "a-user"
        assert a_user.username == "username@server.io"
        assert a_user.check_password(valid_password) is True


class TestAuthenticateUserService:

    def test_when_authenticate_is_successful(self, user_service, valid_password):
        user_service.create(
            name="a-user", username="username@server.io", password=valid_password
        )

        a_user = user_service.authenticate(
            username="username@server.io", password=valid_password
        )

        assert a_user.name == "a-user"
        assert a_user.check_password(valid_password) is True
