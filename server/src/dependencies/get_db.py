from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from src.database import get_database_settings

settings = get_database_settings()

engine = create_engine(
    settings.database_url,
)


def get_db() -> Generator[Connection, None, None]:
    """Provide a database connection to the request handler.

    Yields a raw SQLAlchemy Connection. In tests, this dependency is overridden
    by conftest.py to point at a temporary database.
    """

    with engine.connect() as connection:
        yield connection
