#!/usr/bin/env python3
"""Database migration script."""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from alembic.config import Config
from alembic import command
from backend.shared.config import settings


def run_migrations():
    """Run database migrations."""
    # Set up Alembic configuration
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    
    # Update the database URL
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    
    print(f"Running migrations for database: {settings.database_url}")
    
    try:
        # Run migrations
        command.upgrade(alembic_cfg, "head")
        print("✅ Migrations completed successfully!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)


def create_migration(message: str):
    """Create a new migration."""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    
    try:
        command.revision(alembic_cfg, message=message, autogenerate=True)
        print(f"✅ Migration created: {message}")
    except Exception as e:
        print(f"❌ Failed to create migration: {e}")
        sys.exit(1)


def downgrade_migration(revision: str):
    """Downgrade to a specific revision."""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    
    try:
        command.downgrade(alembic_cfg, revision)
        print(f"✅ Downgraded to revision: {revision}")
    except Exception as e:
        print(f"❌ Failed to downgrade: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python migrate.py upgrade          # Run all migrations")
        print("  python migrate.py create <message> # Create new migration")
        print("  python migrate.py downgrade <rev>  # Downgrade to revision")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "upgrade":
        run_migrations()
    elif action == "create" and len(sys.argv) > 2:
        create_migration(sys.argv[2])
    elif action == "downgrade" and len(sys.argv) > 2:
        downgrade_migration(sys.argv[2])
    else:
        print("Invalid command. Use 'upgrade', 'create <message>', or 'downgrade <revision>'")
        sys.exit(1)