import logging
from server.worker.constant import CHUNK_SIZE
from server.worker.process_csv_file_chunk import process_csv_file_chunk_task
from server.worker.utils import get_line_count
from .celery import app

logger = logging.getLogger(__name__)


@app.task()
def process_csv_file_task(*, file_path: str, db_config: dict):
    # NOTE: minus 1 for the header
    line_count = get_line_count(file_path) - 1
    chunk_index = 0
    for i in range(0, line_count, CHUNK_SIZE):
        process_csv_file_chunk_task.delay(
            file_path=file_path, db_config=db_config, chunk_index=chunk_index
        )
        chunk_index += 1
