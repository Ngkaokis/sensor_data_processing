from sqlalchemy.orm import Session
from celery import Celery
from server.config import app_config
import csv

from server.models import open_db_session
from server.models.sensor import Sensor
from server.models.sensor_reading import SensorReading
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

app = Celery("worker", broker=app_config.broker_url)


def get_sensor_by_name(session: Session, name: str) -> Sensor | None:
    stmt = select(Sensor).where(Sensor.name == name)

    return session.scalar(stmt)


def parse_row(row: dict):
    try:
        return {
            "sensor_name": row["sensorName"],
            "timestamp": datetime.fromisoformat(row["timestamp"]),
            "value": float(row["value"]),
        }
    except Exception as e:
        print(e)
        return None


@app.task
def process_csv_file_task(*, file_path: str):
    with open_db_session() as session:
        records = []
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                parsed_row = parse_row(row)
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
        insert_stmt = insert(SensorReading).values(records).on_conflict_do_nothing()
        session.execute(insert_stmt)
