"""mealplan position

Revision ID: 8a43cdcddd1a
Revises: b179e6c3313b
Create Date: 2022-08-23 21:46:36.550328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8a43cdcddd1a"
down_revision = "b179e6c3313b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("mealplan", sa.Column("position", sa.Integer()))

    op.execute(
        "UPDATE mealplan "
        "SET position = temp.row "
        "FROM ("
        "SELECT id, ROW_NUMBER() OVER (PARTITION BY date) row FROM mealplan"
        ") AS temp "
        "WHERE mealplan.id = temp.id"
    )

    with op.batch_alter_table("mealplan") as batch_op:
        batch_op.alter_column("position", nullable=False)
        batch_op.create_unique_constraint(
            "mealplan_position_unique", ["id", "position"]
        )


def downgrade() -> None:
    with op.batch_alter_table("mealplan") as batch_op:
        batch_op.drop_constraint("mealplan_position_unique", type_="unique")
        batch_op.drop_column("position")
