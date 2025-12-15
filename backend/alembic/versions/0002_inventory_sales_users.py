"""add inventory, sales, users, roles with constraints

Revision ID: 0002
Revises: 0001
Create Date: 2025-12-15
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Role table
    op.create_table(
        'role',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True, index=True),
        sa.Column('description', sa.String(length=200), nullable=True),
    )
    op.create_index('ix_role_id', 'role', ['id'])
    op.create_index('ix_role_name', 'role', ['name'], unique=True)

    # User table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column('email', sa.String(length=320), nullable=True, unique=True, index=True),
        sa.Column('password_hash', sa.String(length=200), nullable=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.id'), nullable=False, index=True),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_user_id', 'user', ['id'])
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    op.create_index('ix_user_email', 'user', ['email'], unique=True)

    # Product table (Inventory)
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False, index=True),
        sa.Column('sku', sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('price', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_product_id', 'product', ['id'])
    op.create_index('ix_product_name', 'product', ['name'])
    op.create_index('ix_product_sku', 'product', ['sku'], unique=True)
    # Check constraint: price >= 0
    op.create_check_constraint('ck_product_price_positive', 'product', 'price >= 0')
    # Check constraint: stock >= 0
    op.create_check_constraint('ck_product_stock_nonnegative', 'product', 'stock >= 0')

    # SaleOrder table
    op.create_table(
        'sale_order',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_number', sa.String(length=50), nullable=False, unique=True, index=True),
        sa.Column('contact_id', sa.Integer(), sa.ForeignKey('contact.id'), nullable=True, index=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('total', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_sale_order_id', 'sale_order', ['id'])
    op.create_index('ix_sale_order_order_number', 'sale_order', ['order_number'], unique=True)
    op.create_check_constraint('ck_sale_order_total_nonnegative', 'sale_order', 'total >= 0')
    op.create_check_constraint(
        'ck_sale_order_status',
        'sale_order',
        "status IN ('draft', 'confirmed', 'shipped', 'invoiced', 'cancelled')"
    )

    # OrderItem table
    op.create_table(
        'order_item',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('sale_order.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('product.id'), nullable=True, index=True),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('subtotal', sa.Numeric(12, 2), nullable=False, server_default='0'),
    )
    op.create_index('ix_order_item_id', 'order_item', ['id'])
    op.create_check_constraint('ck_order_item_quantity_positive', 'order_item', 'quantity > 0')
    op.create_check_constraint('ck_order_item_unit_price_nonnegative', 'order_item', 'unit_price >= 0')
    op.create_check_constraint('ck_order_item_subtotal_nonnegative', 'order_item', 'subtotal >= 0')


def downgrade() -> None:
    op.drop_table('order_item')
    op.drop_table('sale_order')
    op.drop_table('product')
    op.drop_table('user')
    op.drop_table('role')
