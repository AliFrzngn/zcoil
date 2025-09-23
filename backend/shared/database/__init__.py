"""Database configuration and utilities."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, NullPool

from ..config import settings

# Create database engine with proper connection pooling
if "sqlite" in settings.database_url:
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        poolclass=NullPool,  # SQLite doesn't support connection pooling
        connect_args={"check_same_thread": False},
        echo=settings.debug,
    )
else:
    # PostgreSQL/MySQL configuration with connection pooling
    engine = create_engine(
        settings.database_url,
        poolclass=QueuePool,
        pool_size=10,  # Number of connections to maintain in the pool
        max_overflow=20,  # Additional connections that can be created on demand
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,  # Recycle connections after 1 hour
        echo=settings.debug,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db():
    """Get database session with proper error handling."""
    db = SessionLocal()
    try:
        # Test connection health
        db.execute("SELECT 1")
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db_session():
    """Get database session for non-dependency usage."""
    return SessionLocal()


def check_db_health() -> bool:
    """Check database connection health."""
    try:
        db = get_db_session()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception:
        return False


def create_tables():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables."""
    Base.metadata.drop_all(bind=engine)
<<<<<<< Current (Your changes)
<<<<<<< Current (Your changes)
>>>>>>> Incoming (Background Agent changes)
=======
>>>>>>> Incoming (Background Agent changes)
=======
>>>>>>> Incoming (Background Agent changes)
