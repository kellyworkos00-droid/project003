"""init contacts and deals

Revision ID: 0001
Revises: 
Create Date: 2025-12-15
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'contact',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False, index=True),
        sa.Column('email', sa.String(length=320), nullable=True, index=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('company', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_contact_id', 'contact', ['id'])
    op.create_index('ix_contact_name', 'contact', ['name'])
    op.create_index('ix_contact_email', 'contact', ['email'])

    op.create_table(
        'deal',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('stage', sa.String(length=50), nullable=True),
        sa.Column('contact_id', sa.Integer(), sa.ForeignKey('contact.id'), index=True, nullable=True),
    )
    op.create_index('ix_deal_id', 'deal', ['id'])
    op.create_index('ix_deal_title', 'deal', ['title'])


def downgrade() -> None:
    op.drop_index('ix_deal_title', table_name='deal')
    op.drop_index('ix_deal_id', table_name='deal')
    op.drop_table('deal')

    op.drop_index('ix_contact_email', table_name='contact')
    op.drop_index('ix_contact_name', table_name='contact')
    op.drop_index('ix_contact_id', table_name='contact')
    op.drop_table('contact')
