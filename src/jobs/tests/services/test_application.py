import pytest

from ...models.application import Application
from ...models.job import Job
from ...models.organization import Organization
from ...models.user import User
from ...utils.application import ApplicationState
from ...utils.job import JobContract, JobMode


class TestApplicationService:

    def test_when_create_is_successful(self, application_service, valid_password):
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

        application_service.create(
            job_id=a_job.id,
            user_id=a_user.id,
        )

        assert application_service.session.query(Application).count() == 1

        an_application = application_service.session.query(Application).one()
        assert an_application.state == ApplicationState.DRAFT
        assert an_application.job_id == a_job.id
        assert an_application.user_id == a_user.id
