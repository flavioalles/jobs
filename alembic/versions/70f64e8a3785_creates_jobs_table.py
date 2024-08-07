"""Creates jobs table.

Revision ID: 70f64e8a3785
Revises: d3bc93a496e7
Create Date: 2024-06-16 15:53:15.361633+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "70f64e8a3785"
down_revision: Union[str, None] = "d3bc93a496e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "jobs",
        sa.Column("title", sa.Unicode(length=255), nullable=False),
        sa.Column("description", sa.UnicodeText(), nullable=True),
        sa.Column(
            "state",
            sa.Enum("DRAFT", "OPEN", "CLOSED", "CANCELLED", "DONE", name="jobstate"),
            nullable=False,
        ),
        sa.Column("salary", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "mode",
            sa.Enum("HYBRID", "ON_SITE", "REMOTE", name="jobmode"),
            nullable=False,
        ),
        sa.Column(
            "contract",
            sa.Enum("FULL_TIME", "PART_TIME", "TEMPORARY", name="jobcontract"),
            nullable=False,
        ),
        sa.Column("organization_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jobs_contract"), "jobs", ["contract"], unique=False)
    op.create_index(op.f("ix_jobs_id"), "jobs", ["id"], unique=True)
    op.create_index(op.f("ix_jobs_mode"), "jobs", ["mode"], unique=False)
    op.create_index(op.f("ix_jobs_salary"), "jobs", ["salary"], unique=False)
    op.create_index(op.f("ix_jobs_state"), "jobs", ["state"], unique=False)
    op.create_index(op.f("ix_jobs_title"), "jobs", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_jobs_title"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_state"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_salary"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_mode"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_id"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_contract"), table_name="jobs")
    op.drop_table("jobs")
    # ### end Alembic commands ###
