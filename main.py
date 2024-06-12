from server.worker import process_csv_file_task

if __name__ == "__main__":
    process_csv_file_task.delay()
