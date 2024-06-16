import os
import logging
from server.config import app_config


def get_log_level():
    if app_config.log_level == "CRITICAL":
        return logging.CRITICAL
    elif app_config.log_level == "FATAL":
        return logging.FATAL
    elif app_config.log_level == "ERROR":
        return logging.ERROR
    elif app_config.log_level == "WARNING":
        return logging.WARNING
    elif app_config.log_level == "WARN":
        return logging.WARN
    elif app_config.log_level == "INFO":
        return logging.INFO
    elif app_config.log_level == "DEBUG":
        return logging.DEBUG
    else:
        return logging.NOTSET


def get_line_count(file_path):
    with open(file_path, "rb") as f:
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.raw.read
        buf = read_f(buf_size)
        while buf:
            lines += buf.count(b"\n")
            buf = read_f(buf_size)
        return lines
