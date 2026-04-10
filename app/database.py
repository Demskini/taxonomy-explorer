"""
Database setup for the taxonomy explorer project.

This file creates the SQLite engine and provides helper functions
for creating tables and opening database sessions.
"""

from sqlmodel import SQLModel, create_engine, Session

# SQLite database file for the project
DATABASE_URL = "sqlite:///taxonomy.db"

# Create the database connection object
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    """Create all database tables defined in the SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Return a new database session."""
    return Session(engine)