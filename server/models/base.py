from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, BigInteger, Identity, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from pydantic import AwareDatetime
from server.config import app_config


class Base(DeclarativeBase, MappedAsDataclass):
    metadata = MetaData(
        schema=app_config.db_schema,
        naming_convention={
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s",
            "pk": "pk_%(table_name)s",
        },
    )

    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
        AwareDatetime: TIMESTAMP(timezone=True),
    }

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(start=1001), init=False, primary_key=True, sort_order=-1
    )

    created_at: Mapped[AwareDatetime] = mapped_column(
        init=False, default_factory=lambda: datetime.now(UTC), sort_order=-1
    )

    def values(self, *, exclude: set[str] | None = None):
        return {
            k: getattr(self, k)
            for k in self.__mapper__.columns.keys()
            if exclude is None or k not in exclude
        }
