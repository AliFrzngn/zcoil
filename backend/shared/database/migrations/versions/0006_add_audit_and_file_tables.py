"""Add audit and file upload tables

Revision ID: 0006
Revises: 0005
Create Date: 2024-01-01 00:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=100), nullable=False),
        sa.Column('resource_id', sa.String(length=100), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_resource_type'), 'audit_logs', ['resource_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_resource_id'), 'audit_logs', ['resource_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)

    # Create file_uploads table
    op.create_table('file_uploads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('content_type', sa.String(length=100), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('resource_type', sa.String(length=100), nullable=True),
        sa.Column('resource_id', sa.String(length=100), nullable=True),
        sa.Column('is_public', sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_uploads_id'), 'file_uploads', ['id'], unique=False)
    op.create_index(op.f('ix_file_uploads_user_id'), 'file_uploads', ['user_id'], unique=False)
    op.create_index(op.f('ix_file_uploads_resource_type'), 'file_uploads', ['resource_type'], unique=False)
    op.create_index(op.f('ix_file_uploads_resource_id'), 'file_uploads', ['resource_id'], unique=False)
    op.create_index(op.f('ix_file_uploads_created_at'), 'file_uploads', ['created_at'], unique=False)

    # Add foreign key constraints
    op.create_foreign_key('fk_audit_logs_user_id', 'audit_logs', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_file_uploads_user_id', 'file_uploads', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('fk_file_uploads_user_id', 'file_uploads', type_='foreignkey')
    op.drop_constraint('fk_audit_logs_user_id', 'audit_logs', type_='foreignkey')

    # Drop file_uploads table
    op.drop_index(op.f('ix_file_uploads_created_at'), table_name='file_uploads')
    op.drop_index(op.f('ix_file_uploads_resource_id'), table_name='file_uploads')
    op.drop_index(op.f('ix_file_uploads_resource_type'), table_name='file_uploads')
    op.drop_index(op.f('ix_file_uploads_user_id'), table_name='file_uploads')
    op.drop_index(op.f('ix_file_uploads_id'), table_name='file_uploads')
    op.drop_table('file_uploads')

    # Drop audit_logs table
    op.drop_index(op.f('ix_audit_logs_created_at'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_resource_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_resource_type'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_id'), table_name='audit_logs')
    op.drop_table('audit_logs')