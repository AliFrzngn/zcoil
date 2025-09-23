"""Add sample data

Revision ID: 0004
Revises: 0003
Create Date: 2024-01-01 00:03:00.000000

"""
from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    # Create sample users
    users_table = sa.table('users',
        sa.column('id', sa.Integer),
        sa.column('email', sa.String),
        sa.column('username', sa.String),
        sa.column('hashed_password', sa.String),
        sa.column('full_name', sa.String),
        sa.column('is_active', sa.Boolean),
        sa.column('is_verified', sa.Boolean),
        sa.column('is_superuser', sa.Boolean),
        sa.column('role', sa.String),
        sa.column('phone', sa.String),
        sa.column('bio', sa.String)
    )

    # Insert sample users
    op.bulk_insert(users_table, [
        {
            'email': 'admin@alifrzngn.dev',
            'username': 'admin',
            'hashed_password': pwd_context.hash('Admin123!'),
            'full_name': 'System Administrator',
            'is_active': True,
            'is_verified': True,
            'is_superuser': True,
            'role': 'admin',
            'phone': '+1234567890',
            'bio': 'System administrator for AliFrzngn Development'
        },
        {
            'email': 'manager@alifrzngn.dev',
            'username': 'manager',
            'hashed_password': pwd_context.hash('Manager123!'),
            'full_name': 'Manager User',
            'is_active': True,
            'is_verified': True,
            'is_superuser': False,
            'role': 'manager',
            'phone': '+1234567891',
            'bio': 'Manager for AliFrzngn Development'
        },
        {
            'email': 'customer@alifrzngn.dev',
            'username': 'customer',
            'hashed_password': pwd_context.hash('Customer123!'),
            'full_name': 'Test Customer',
            'is_active': True,
            'is_verified': True,
            'is_superuser': False,
            'role': 'customer',
            'phone': '+1234567892',
            'bio': 'Test customer account'
        }
    ])

    # Create sample products
    products_table = sa.table('products',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('description', sa.String),
        sa.column('sku', sa.String),
        sa.column('price', sa.Float),
        sa.column('cost', sa.Float),
        sa.column('quantity', sa.Integer),
        sa.column('min_quantity', sa.Integer),
        sa.column('max_quantity', sa.Integer),
        sa.column('is_active', sa.Boolean),
        sa.column('category', sa.String),
        sa.column('brand', sa.String),
        sa.column('weight', sa.Float),
        sa.column('dimensions', sa.String),
        sa.column('customer_id', sa.String)
    )

    # Insert sample products
    op.bulk_insert(products_table, [
        {
            'name': 'Laptop Pro 15"',
            'description': 'High-performance laptop with 15-inch display',
            'sku': 'LAPTOP-PRO-15',
            'price': 1299.99,
            'cost': 800.00,
            'quantity': 50,
            'min_quantity': 10,
            'max_quantity': 100,
            'is_active': True,
            'category': 'Electronics',
            'brand': 'TechBrand',
            'weight': 2.5,
            'dimensions': '35x25x2',
            'customer_id': 'customer-123'
        },
        {
            'name': 'Wireless Mouse',
            'description': 'Ergonomic wireless mouse with Bluetooth connectivity',
            'sku': 'MOUSE-WIRELESS-001',
            'price': 29.99,
            'cost': 15.00,
            'quantity': 200,
            'min_quantity': 20,
            'max_quantity': 500,
            'is_active': True,
            'category': 'Accessories',
            'brand': 'TechBrand',
            'weight': 0.1,
            'dimensions': '12x6x4',
            'customer_id': 'customer-123'
        },
        {
            'name': 'Mechanical Keyboard',
            'description': 'RGB mechanical keyboard with Cherry MX switches',
            'sku': 'KEYBOARD-MECH-001',
            'price': 149.99,
            'cost': 80.00,
            'quantity': 75,
            'min_quantity': 15,
            'max_quantity': 200,
            'is_active': True,
            'category': 'Accessories',
            'brand': 'TechBrand',
            'weight': 1.2,
            'dimensions': '45x15x3',
            'customer_id': 'customer-456'
        },
        {
            'name': 'Monitor 27" 4K',
            'description': '27-inch 4K UHD monitor with HDR support',
            'sku': 'MONITOR-27-4K',
            'price': 399.99,
            'cost': 250.00,
            'quantity': 30,
            'min_quantity': 5,
            'max_quantity': 100,
            'is_active': True,
            'category': 'Electronics',
            'brand': 'DisplayPro',
            'weight': 6.5,
            'dimensions': '62x37x5',
            'customer_id': 'customer-789'
        }
    ])

    # Create sample notification templates
    templates_table = sa.table('notification_templates',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('type', sa.String),
        sa.column('channel', sa.String),
        sa.column('subject_template', sa.String),
        sa.column('body_template', sa.String),
        sa.column('is_active', sa.Boolean),
        sa.column('variables', sa.JSON)
    )

    # Insert sample notification templates
    op.bulk_insert(templates_table, [
        {
            'name': 'welcome_email',
            'type': 'welcome',
            'channel': 'email',
            'subject_template': 'Welcome to AliFrzngn Development!',
            'body_template': 'Hello {{full_name}},\n\nWelcome to AliFrzngn Development! We are excited to have you on board.\n\nBest regards,\nThe AliFrzngn Team',
            'is_active': True,
            'variables': '["full_name", "email"]'
        },
        {
            'name': 'low_stock_alert',
            'type': 'inventory',
            'channel': 'email',
            'subject_template': 'Low Stock Alert: {{product_name}}',
            'body_template': 'Product {{product_name}} (SKU: {{sku}}) is running low on stock. Current quantity: {{quantity}}, Minimum required: {{min_quantity}}',
            'is_active': True,
            'variables': '["product_name", "sku", "quantity", "min_quantity"]'
        },
        {
            'name': 'order_confirmation',
            'type': 'order',
            'channel': 'email',
            'subject_template': 'Order Confirmation #{{order_id}}',
            'body_template': 'Thank you for your order! Order #{{order_id}} has been confirmed and will be processed shortly.\n\nOrder Total: ${{total_amount}}\n\nItems:\n{{items_list}}',
            'is_active': True,
            'variables': '["order_id", "total_amount", "items_list"]'
        }
    ])


def downgrade() -> None:
    # Delete sample data
    op.execute("DELETE FROM notification_templates WHERE name IN ('welcome_email', 'low_stock_alert', 'order_confirmation')")
    op.execute("DELETE FROM products WHERE sku IN ('LAPTOP-PRO-15', 'MOUSE-WIRELESS-001', 'KEYBOARD-MECH-001', 'MONITOR-27-4K')")
    op.execute("DELETE FROM users WHERE email IN ('admin@alifrzngn.dev', 'manager@alifrzngn.dev', 'customer@alifrzngn.dev')")
