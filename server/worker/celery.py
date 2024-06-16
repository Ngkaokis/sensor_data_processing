import logging
from celery import Celery
from celery.signals import after_setup_logger
from server.config import app_config

from server.worker.utils import get_log_level

app = Celery("worker", broker=app_config.broker_url)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    fh = logging.FileHandler(app_config.log_file or "logs/celery.log")
    fh.setLevel(get_log_level())

    formatter = logging.Formatter(
        "%(asctime)s  %(levelname)s  [pid:%(process)d] [%(name)s %(filename)s->%(funcName)s:%(lineno)s] %(message)s"
    )
    fh.setFormatter(formatter)

    logger.addHandler(fh)
