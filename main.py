import os
import argparse
from celery import Celery

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process CSV files and insert sensor readings into the database."
    )
    parser.add_argument(
        "directory", type=str, help="The target directory containing CSV files"
    )
    parser.add_argument("--dbhost", type=str, help="Database host")
    parser.add_argument("--dbname", type=str, help="Database name")
    parser.add_argument("--dbuser", type=str, help="Database user")
    parser.add_argument("--dbpass", type=str, help="Database password")
    parser.add_argument("--dbport", type=str, help="Database port")

    args = parser.parse_args()

    app = Celery(
        "worker",
        broker=os.environ.get("BROKER_URL", ""),
    )
    for filename in os.listdir(args.directory):
        f = os.path.join(args.directory, filename)
        if os.path.isfile(f):
            app.send_task(
                "server.worker.celery.process_csv_file_task",
                kwargs={
                    "file_path": f,
                    "db_config": {
                        "host": args.dbhost,
                        "port": args.dbport,
                        "user": args.dbuser,
                        "password": args.dbpass,
                        "name": args.dbname,
                    },
                },
            )
