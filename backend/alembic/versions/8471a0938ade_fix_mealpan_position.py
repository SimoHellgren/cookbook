"""fix_mealpan_position

Revision ID: 8471a0938ade
Revises: 8a43cdcddd1a
Create Date: 2022-09-09 23:25:44.865934

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "8471a0938ade"
down_revision = "8a43cdcddd1a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("mealplan") as batch_op:
        batch_op.drop_constraint("mealplan_position_unique", type_="unique")
        batch_op.create_unique_constraint(
            "mealplan_position_unique", ["date", "position"]
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("mealplan") as batch_op:
        batch_op.drop_constraint("mealplan_position_unique", type_="unique")
        batch_op.create_unique_constraint(
            "mealplan_position_unique", ["id", "position"]
        )
    # ### end Alembic commands ###
