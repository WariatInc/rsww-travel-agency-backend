"""Create user and user identity table

Revision ID: 6e80b58d4007
Revises: 
Create Date: 2023-04-16 21:02:02.587670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e80b58d4007'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('gid', sa.UUID(), nullable=False),
    sa.Column('_created', sa.DateTime(), nullable=True),
    sa.Column('_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_identity',
    sa.Column('gid', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_created', sa.DateTime(), nullable=True),
    sa.Column('_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('gid')
    )


def downgrade():
    op.drop_table('user_identity')
    op.drop_table('user')
