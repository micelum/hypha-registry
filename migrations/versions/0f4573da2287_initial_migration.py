"""initial migration

Revision ID: 0f4573da2287
Revises: 
Create Date: 2021-08-08 19:26:54.496428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f4573da2287'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'known_devices',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('machine_uuid', sa.String, nullable=False),
        sa.Column('machine_mac', sa.String, nullable=False),
        sa.Column('type', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now()),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.UniqueConstraint('machine_uuid', 'machine_mac', 'is_active', name='uc_user_machine_active')
    )

def downgrade():
    op.drop_table('known_devices')
