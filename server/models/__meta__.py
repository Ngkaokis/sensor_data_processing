from collections.abc import Iterator
from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from typing import Optional

import sqlalchemy as sa

from server.models.db_config import DbConfig


def create_app_engine(db_url: Optional[str] = None):
    return sa.create_engine(
        db_url or DbConfig().db_url(),
    )


@contextmanager
def open_db_session(db_url: Optional[str] = None, read_write=True) -> Iterator[Session]:
    engine = create_app_engine(db_url)

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
