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
