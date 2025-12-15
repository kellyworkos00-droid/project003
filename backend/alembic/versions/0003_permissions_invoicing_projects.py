"""add permissions, invoicing, projects modules

Revision ID: 0003
Revises: 0002
Create Date: 2025-12-15
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Permission table
    op.create_table(
        'permission',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column('description', sa.String(length=200), nullable=True),
    )
    op.create_index('ix_permission_id', 'permission', ['id'])
    op.create_index('ix_permission_name', 'permission', ['name'], unique=True)

    # RolePermission junction table
    op.create_table(
        'role_permission',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('permission_id', sa.Integer(), sa.ForeignKey('permission.id', ondelete='CASCADE'), nullable=False, index=True),
    )
    op.create_index('ix_role_permission_id', 'role_permission', ['id'])

    # Invoice table
    op.create_table(
        'invoice',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('invoice_number', sa.String(length=50), nullable=False, unique=True, index=True),
        sa.Column('sale_order_id', sa.Integer(), sa.ForeignKey('sale_order.id'), nullable=True, index=True),
        sa.Column('contact_id', sa.Integer(), sa.ForeignKey('contact.id'), nullable=True, index=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('invoice_date', sa.Date(), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('subtotal', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('tax', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('total', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_invoice_id', 'invoice', ['id'])
    op.create_index('ix_invoice_invoice_number', 'invoice', ['invoice_number'], unique=True)
    op.create_check_constraint('ck_invoice_subtotal_nonnegative', 'invoice', 'subtotal >= 0')
    op.create_check_constraint('ck_invoice_tax_nonnegative', 'invoice', 'tax >= 0')
    op.create_check_constraint('ck_invoice_total_nonnegative', 'invoice', 'total >= 0')
    op.create_check_constraint(
        'ck_invoice_status',
        'invoice',
        "status IN ('draft', 'sent', 'paid', 'cancelled')"
    )

    # InvoiceItem table
    op.create_table(
        'invoice_item',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('invoice_id', sa.Integer(), sa.ForeignKey('invoice.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('product.id'), nullable=True, index=True),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('subtotal', sa.Numeric(12, 2), nullable=False, server_default='0'),
    )
    op.create_index('ix_invoice_item_id', 'invoice_item', ['id'])
    op.create_check_constraint('ck_invoice_item_quantity_positive', 'invoice_item', 'quantity > 0')

    # Project table
    op.create_table(
        'project',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False, index=True),
        sa.Column('code', sa.String(length=50), nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('contact_id', sa.Integer(), sa.ForeignKey('contact.id'), nullable=True, index=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='active'),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_project_id', 'project', ['id'])
    op.create_index('ix_project_name', 'project', ['name'])
    op.create_index('ix_project_code', 'project', ['code'], unique=True)
    op.create_check_constraint(
        'ck_project_status',
        'project',
        "status IN ('active', 'on_hold', 'completed', 'cancelled')"
    )

    # Task table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('project.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('assigned_to_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=True, index=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='todo'),
        sa.Column('priority', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_task_id', 'task', ['id'])
    op.create_check_constraint(
        'ck_task_status',
        'task',
        "status IN ('todo', 'in_progress', 'review', 'done')"
    )
    op.create_check_constraint(
        'ck_task_priority',
        'task',
        "priority IN ('low', 'medium', 'high', 'urgent')"
    )

    # TimeSheet table
    op.create_table(
        'time_sheet',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('task.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False, index=True),
        sa.Column('hours', sa.Integer(), nullable=False),  # minutes
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_time_sheet_id', 'time_sheet', ['id'])
    op.create_check_constraint('ck_time_sheet_hours_positive', 'time_sheet', 'hours > 0')


def downgrade() -> None:
    op.drop_table('time_sheet')
    op.drop_table('task')
    op.drop_table('project')
    op.drop_table('invoice_item')
    op.drop_table('invoice')
    op.drop_table('role_permission')
    op.drop_table('permission')
