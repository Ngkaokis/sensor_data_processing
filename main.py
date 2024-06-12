from server.worker import process_csv_file_task
import os

if __name__ == "__main__":
    for filename in os.listdir("data"):
        f = os.path.join("data", filename)
        if os.path.isfile(f):
            process_csv_file_task.delay(
                file_path=f,
            )
