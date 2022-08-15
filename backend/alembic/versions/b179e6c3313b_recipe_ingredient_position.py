"""recipe_ingredient_position

Revision ID: b179e6c3313b
Revises: 931478b39591
Create Date: 2022-08-15 19:09:28.119138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b179e6c3313b'
down_revision = '931478b39591'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("recipe_ingredient", sa.Column('position', sa.Integer()))
    op.execute(
        "UPDATE recipe_ingredient "
        "SET position = temp.row "
        "FROM ("
        "SELECT recipe_id, ingredient_id, ROW_NUMBER() OVER (PARTITION BY recipe_id) row FROM recipe_ingredient"
        ") AS temp "
        "WHERE recipe_ingredient.recipe_id = temp.recipe_id "
        "AND recipe_ingredient.ingredient_id = temp.ingredient_id"

    )

    with op.batch_alter_table("recipe_ingredient") as batch_op:
        batch_op.alter_column("position", nullable=False)
        batch_op.create_unique_constraint('recipeid_position_unique', ['recipe_id', 'position'])


def downgrade() -> None:
    with op.batch_alter_table("recipe_ingredient") as batch_op:
        batch_op.drop_constraint('recipeid_position_unique', type_='unique')
        batch_op.drop_column('position')
