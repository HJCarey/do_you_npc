"""Database configuration and session management."""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base


class DatabaseConfig:
    """Database configuration and connection management."""
    
    def __init__(self, database_url: str = None):
        """Initialize database configuration.
        
        Args:
            database_url: PostgreSQL connection string. If None, reads from environment.
        """
        if database_url is None:
            # Read from environment variables
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "do_you_npc")
            db_user = os.getenv("DB_USER", "jake")
            db_password = os.getenv("DB_PASSWORD", "")
            
            # Use local socket connection for peer authentication if no password
            if not db_password and db_host in ("localhost", "127.0.0.1"):
                database_url = f"postgresql:///{db_name}?user={db_user}&host=/var/run/postgresql"
            else:
                database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        self.engine = create_engine(database_url, echo=os.getenv("DEBUG", "false").lower() == "true")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all database tables."""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session.
        
        Yields:
            Session: SQLAlchemy database session
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


# Global database configuration instance
db_config = DatabaseConfig()


def get_db_session() -> Generator[Session, None, None]:
    """Get a database session (convenience function).
    
    Yields:
        Session: SQLAlchemy database session
    """
    yield from db_config.get_session()