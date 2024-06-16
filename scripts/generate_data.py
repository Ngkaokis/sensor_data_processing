import csv
import random
import argparse
from faker import Faker
from dateutil import tz

parser = argparse.ArgumentParser(description="Generate sensor reading data")
parser.add_argument(
    "--size", type=int, default=1000000, help="number of items to be generated"
)
parser.add_argument("--output", type=str, default="data/data.csv", help="Database port")

args = parser.parse_args()

default_sensor_name = [
    "Temperature Sensor 1",
    "Pressure Sensor 1",
    "Humidity Sensor 1",
    "Light Sensor 1",
    "Motion Sensor 1",
    "Proximity Sensor 1",
    "Accelerometer 1",
    "Gyroscope 1",
    "Magnetic Field Sensor 1",
    "pH Sensor 1",
]

faker = Faker("en_GB")
tzinfo = tz.gettz("Asia/Hong_Kong")
f = open(args.output, "a")
w = csv.writer(f)
w.writerow(("sensorName", "timestamp", "value"))
for i in range(args.size):
    sensor_name = random.choice(default_sensor_name)
    timestamp = faker.iso8601(tzinfo=tzinfo)
    # Generate invalid data
    if random.random() > 0.99:
        timestamp = "invalid timestamp"
    value = random.random() * 1000
    if random.random() > 0.99:
        value = "invalid value"
    w.writerow(
        (
            sensor_name,
            timestamp,
            value,
        )
    )
f.close()
