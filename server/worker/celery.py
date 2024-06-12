from celery import Celery
from server.config import app_config
import csv

app = Celery("worker", broker=app_config.broker_url)


@app.task
def process_csv_file_task(*, file_path: str):
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(", ".join(row))
