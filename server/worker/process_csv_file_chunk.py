import logging
from sqlalchemy.orm import Session
import pandas as pd

from server.models import open_db_session
from server.models.db_config import DbConfig
from server.models.sensor import Sensor
from server.models.sensor_reading import SensorReading
from server.worker.process_csv_file import CHUNK_SIZE
from .celery import app
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)


def get_sensor_by_name(session: Session, name: str) -> Sensor:
    stmt = select(Sensor).where(Sensor.name == name)
    sensor = session.scalar(stmt)
    if sensor is None:
        # NOTE: I expect sensors in use are already in DB. If not, create a new one with unknown sensor type.
        # This is kind of a hacky way to get the sensor and I assume we don't need to do this in real enviroment
        sensor = Sensor(name=name, type="unknown_sensor_type")
        try:
            session.add(sensor)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.exception(f"Sensor {sensor.name} is created  in another worker")
            sensor = session.scalar(stmt)

    return sensor


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


def get_chunk(file_path: str, chunk_index: int, chunksize: int = CHUNK_SIZE):
    index = -1
    with pd.read_csv(file_path, chunksize=chunksize) as chunks:
        for chunk in chunks:
            index += 1
            if index != chunk_index:
                continue

            return chunk


@app.task()
def process_csv_file_chunk_task(*, file_path: str, db_config: dict, chunk_index: int):
    config = DbConfig.from_json(db_config)
    records = []
    # NOTES: pandas skiprows create a giant list if we pass a large number to it. So need to itearte until we reach the target chunk
    chunk = get_chunk(file_path, chunk_index)
    with open_db_session(config.db_url()) as session:
        for index, row in chunk.iterrows():
            parsed_row = parse_row(row, file_path)
            if parsed_row is None:
                continue
            sensor = get_sensor_by_name(session, parsed_row["sensor_name"])

            record = SensorReading(
                value=parsed_row["value"],
                timestamp=parsed_row["timestamp"],
                sensor_id=sensor.id,
                sensor=sensor,
            )
            records.append(record.values(exclude={"id", "sensor"}))
        # NOTE: Use postgresql ability to skip records that violated constriant
        insert_stmt = insert(SensorReading).values(records).on_conflict_do_nothing()
        session.execute(insert_stmt)
