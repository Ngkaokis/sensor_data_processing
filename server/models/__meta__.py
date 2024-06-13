from collections.abc import Iterator
from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager
from typing import Iterator

import sqlalchemy as sa

from ..config import app_config

_db_engine = None


def create_app_engine():
    return sa.create_engine(
        app_config.db_url,
    )


def get_db_engine():
    global _db_engine
    if _db_engine:
        return _db_engine
    _db_engine = create_app_engine()
    return _db_engine


@contextmanager
def open_db_session(read_write=True) -> Iterator[Session]:
    engine = get_db_engine()

    Session = sessionmaker(engine, expire_on_commit=False)
    session = Session()

    try:
        if not read_write:
            session.execute(sa.text("SET TRANSACTION READ ONLY"))
        yield session
        if not read_write or not session.is_active:
            session.rollback()
        else:
            session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()
