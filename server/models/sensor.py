from typing import TYPE_CHECKING, List
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

if TYPE_CHECKING:
    from . import SensorReading


class Sensor(Base):
    __tablename__ = "sensor"

    name: Mapped[str] = mapped_column(Text, nullable=False, index=True, unique=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)

    sensor_readings: Mapped[List["SensorReading"]] = relationship(
        back_populates="sensor", default_factory=lambda: []
    )
