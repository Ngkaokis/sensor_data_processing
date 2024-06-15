import os
from celery import Celery

if __name__ == "__main__":
    app = Celery(
        "worker",
        broker=os.environ.get("BROKER_URL", ""),
    )
    for filename in os.listdir("data"):
        f = os.path.join("data", filename)
        if os.path.isfile(f):
            app.send_task(
                "server.worker.celery.process_csv_file_task",
                kwargs={
                    "file_path": f,
                },
            )
