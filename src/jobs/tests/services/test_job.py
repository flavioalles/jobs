import pytest

from ...models.job import Job
from ...models.organization import Organization
from ...utils.job import JobContract, JobMode, JobState


class TestJobService:

    def test_when_create_is_successful(self, job_service, valid_password):
        job_service.session.add(
            Organization(name="an-organization", password=valid_password)
        )
        job_service.session.flush()
        an_organization = job_service.session.query(Organization).one()

        job_service.create(
            organization_id=an_organization.id,
            title="a-job",
            salary=float(100000),
            mode=JobMode.ON_SITE,
            contract=JobContract.FULL_TIME,
        )

        assert job_service.session.query(Job).count() == 1

        a_job = job_service.session.query(Job).one()
        assert a_job.title == "a-job"
        assert a_job.description is None
        assert a_job.state == JobState.DRAFT
        assert a_job.salary == float(100000)
        assert a_job.mode == JobMode.ON_SITE
        assert a_job.contract == JobContract.FULL_TIME
        assert a_job.organization_id == an_organization.id
