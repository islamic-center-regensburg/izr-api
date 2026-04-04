"""apply versionning to moqsue table

Revision ID: 08c238d3ea48
Revises: 66adfa8a8913
Create Date: 2026-03-22 21:05:15.751153

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "08c238d3ea48"
down_revision: Union[str, Sequence[str], None] = "66adfa8a8913"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Add columns as nullable
    op.add_column(
        "mosques", sa.Column("valid_from", sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.add_column(
        "mosques", sa.Column("valid_to", sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.add_column(
        "mosques",
        sa.Column("update_reason", sa.String(), nullable=True),
    )

    # 2. Fill default values for **existing rows**
    op.execute(
        """
        UPDATE mosques
        SET valid_from = NOW(),
            valid_to = '9999-12-31T00:00:00+00:00'
        WHERE valid_from IS NULL OR valid_to IS NULL
        """
    )

    # 3. Alter columns to NOT NULL
    op.alter_column("mosques", "valid_from", nullable=False)
    op.alter_column("mosques", "valid_to", nullable=False)


def downgrade():
    op.drop_column("mosques", "update_reason")
    op.drop_column("mosques", "valid_to")
    op.drop_column("mosques", "valid_from")
