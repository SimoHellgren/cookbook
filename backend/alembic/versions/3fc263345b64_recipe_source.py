"""recipe source

Revision ID: 3fc263345b64
Revises: 8471a0938ade
Create Date: 2022-09-12 19:42:49.182520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3fc263345b64"
down_revision = "8471a0938ade"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("recipe", sa.Column("source", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("recipe", "source")
    # ### end Alembic commands ###
