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
