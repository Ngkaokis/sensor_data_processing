import logging
from sqlalchemy.orm import Session
import pandas as pd

from server.models import open_db_session
from server.models.db_config import DbConfig
from server.models.sensor import Sensor
from server.models.sensor_reading import SensorReading
from .celery import app
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)

CHUNK_SIZE = 10000


def get_sensor_by_name(session: Session, name: str) -> Sensor | None:
    stmt = select(Sensor).where(Sensor.name == name)

    return session.scalar(stmt)


def parse_row(row: dict, file_path: str):
    try:
        return {
            "sensor_name": row["sensorName"],
            "timestamp": datetime.fromisoformat(row["timestamp"]),
            "value": float(row["value"]),
        }
    except Exception as e:
        logger.exception(f"Failed to parse csv row {row}. File Path: {file_path}")
        return None


@app.task()
def process_csv_file_task(*, file_path: str, db_config: dict):
    config = DbConfig.from_json(db_config)
    records = []
    # NOTE: Chop the csv into chunks to avoid huge transaction
    with pd.read_csv(file_path, chunksize=CHUNK_SIZE) as chunks:
        for chunk in chunks:
            with open_db_session(config.db_url()) as session:
                chunk = chunk.reset_index()
                for index, row in chunk.iterrows():
                    parsed_row = parse_row(row, file_path)
                    if parsed_row is None:
                        continue
                    sensor = get_sensor_by_name(session, parsed_row["sensor_name"])
                    if sensor is None:
                        # NOTE: I expect sensors in use are already in DB. If not, create a new one with unknown sensor type
                        sensor = Sensor(
                            name=parsed_row["sensor_name"], type="unknown_sensor_type"
                        )
                        session.add(sensor)
                        session.commit()

                    record = SensorReading(
                        value=parsed_row["value"],
                        timestamp=parsed_row["timestamp"],
                        sensor_id=sensor.id,
                        sensor=sensor,
                    )
                    records.append(record.values(exclude={"id"}))
                # NOTE: Use postgresql ability to skip records that violated constriant
                insert_stmt = (
                    insert(SensorReading).values(records).on_conflict_do_nothing()
                )
                session.execute(insert_stmt)
