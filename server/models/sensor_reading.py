from typing import TYPE_CHECKING
from sqlalchemy import TIMESTAMP, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship
from pydantic import AwareDatetime


from .base import Base

if TYPE_CHECKING:
    from . import Sensor


class SensorReading(Base):
    __tablename__ = "sensor_reading"

    @classmethod
    @declared_attr.directive
    def __table_args__(cls):
        return (
            UniqueConstraint(
                "sensor_id",
                "timestamp",
                name="uq_sensor_reading_sensor_id_timestamp",
            ),
        )

    timestamp: Mapped[AwareDatetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    value: Mapped[float] = mapped_column(Numeric, nullable=False)

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensor.id"), index=True, nullable=True
    )
    sensor: Mapped["Sensor"] = relationship(back_populates="sensor_readings")
