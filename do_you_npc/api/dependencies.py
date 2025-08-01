"""FastAPI dependencies for database session management."""

from typing import Generator

from sqlalchemy.orm import Session

from do_you_npc.db.database import get_db_session


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency."""
    yield from get_db_session()