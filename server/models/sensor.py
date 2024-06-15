from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


class Sensor(Base):
    __tablename__ = "sensor"

    name: Mapped[str] = mapped_column(Text, nullable=False, index=True, unique=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
