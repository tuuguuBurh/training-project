"""update user model with role and name

Revision ID: bf5a982230e0
Revises: ce82c1178834
Create Date: 2026-06-22 12:14:57.512937

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bf5a982230e0'
down_revision = 'ce82c1178834'
branch_labels = None
depends_on = None


def upgrade():
    # Create the enum type first
    user_role_enum = sa.Enum('USER', 'APPROVER', 'ADMIN', name='user_role')
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('users', sa.Column('name', sa.String(), nullable=False, server_default=''))
    op.add_column('users', sa.Column('role', user_role_enum, server_default='USER', nullable=False))
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')


def downgrade():
    op.add_column('users', sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'role')
    op.drop_column('users', 'name')

    user_role_enum = sa.Enum('USER', 'APPROVER', 'ADMIN', name='user_role')
    user_role_enum.drop(op.get_bind(), checkfirst=True)
