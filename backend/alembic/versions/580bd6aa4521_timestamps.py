"""timestamps

Revision ID: 580bd6aa4521
Revises: 5f1c118b893f
Create Date: 2022-09-17 12:10:26.885830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '580bd6aa4521'
down_revision = '5f1c118b893f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('comment', sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('ingredient', sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('ingredient', sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('mealplan', sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('mealplan', sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('recipe', sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('recipe', sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('recipe_ingredient', sa.Column('created', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    op.add_column('recipe_ingredient', sa.Column('updated', sa.DateTime(), server_default=sa.text("(now() at time zone 'utc')"), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe_ingredient', 'updated')
    op.drop_column('recipe_ingredient', 'created')
    op.drop_column('recipe', 'updated')
    op.drop_column('recipe', 'created')
    op.drop_column('mealplan', 'updated')
    op.drop_column('mealplan', 'created')
    op.drop_column('ingredient', 'updated')
    op.drop_column('ingredient', 'created')
    op.drop_column('comment', 'updated')
    op.drop_column('comment', 'created')
    # ### end Alembic commands ###
