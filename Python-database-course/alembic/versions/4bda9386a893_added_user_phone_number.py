"""added user phone number

Revision ID: 4bda9386a893
Revises: beb91908ea91
Create Date: 2024-02-21 14:25:37.921881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bda9386a893'
down_revision = 'beb91908ea91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(length=3000),
               nullable=True)
    op.add_column('users', sa.Column('username', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(length=50), nullable=True))
    op.drop_column('users', 'user_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'username')
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(length=3000),
               nullable=False)
    # ### end Alembic commands ###
