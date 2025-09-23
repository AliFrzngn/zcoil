"""Database configuration and utilities."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables."""
<<<<<<< Current (Your changes)
<<<<<<< Current (Your changes)
<<<<<<< Current (Your changes)
<<<<<<< Current (Your changes)
<<<<<<< Current (Your changes)
    Base.metadata.drop_all(bind=engine)
=======
    Base.metadata.drop_all(bind=engine)
>>>>>>> Incoming (Background Agent changes)
=======
    Base.metadata.drop_all(bind=engine)
>>>>>>> Incoming (Background Agent changes)
=======
    Base.metadata.drop_all(bind=engine)
>>>>>>> Incoming (Background Agent changes)
=======
    Base.metadata.drop_all(bind=engine)
>>>>>>> Incoming (Background Agent changes)
=======
    Base.metadata.drop_all(bind=engine)
>>>>>>> Incoming (Background Agent changes)
