"""Add indexes and constraints

Revision ID: 0003
Revises: 0002
Create Date: 2024-01-01 00:02:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add foreign key constraints
    op.create_foreign_key('fk_notifications_user_id', 'notifications', 'users', ['user_id'], ['id'])

    # Add check constraints
    op.create_check_constraint(
        'ck_users_email_format',
        'users',
        "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"
    )
    
    op.create_check_constraint(
        'ck_products_price_positive',
        'products',
        'price > 0'
    )
    
    op.create_check_constraint(
        'ck_products_quantity_non_negative',
        'products',
        'quantity >= 0'
    )
    
    op.create_check_constraint(
        'ck_products_min_quantity_non_negative',
        'products',
        'min_quantity >= 0'
    )

    # Add additional indexes for better performance
    op.create_index('ix_products_price', 'products', ['price'])
    op.create_index('ix_products_quantity', 'products', ['quantity'])
    op.create_index('ix_products_created_at', 'products', ['created_at'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])
    op.create_index('ix_users_last_login', 'users', ['last_login'])
    op.create_index('ix_notifications_created_at', 'notifications', ['created_at'])
    op.create_index('ix_notifications_sent_at', 'notifications', ['sent_at'])


def downgrade() -> None:
    # Drop additional indexes
    op.drop_index('ix_notifications_sent_at', table_name='notifications')
    op.drop_index('ix_notifications_created_at', table_name='notifications')
    op.drop_index('ix_users_last_login', table_name='users')
    op.drop_index('ix_users_created_at', table_name='users')
    op.drop_index('ix_products_created_at', table_name='products')
    op.drop_index('ix_products_quantity', table_name='products')
    op.drop_index('ix_products_price', table_name='products')

    # Drop check constraints
    op.drop_constraint('ck_products_min_quantity_non_negative', 'products')
    op.drop_constraint('ck_products_quantity_non_negative', 'products')
    op.drop_constraint('ck_products_price_positive', 'products')
    op.drop_constraint('ck_users_email_format', 'users')

    # Drop foreign key constraints
    op.drop_constraint('fk_notifications_user_id', 'notifications', type_='foreignkey')