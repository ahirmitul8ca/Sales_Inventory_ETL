from logger_config import setup_logging
from file_manager import ensure_directories


def init_fsys():

    # Initialize the daily logging configuration ONCE
    ensure_directories(['logs', 'exports', 'data'])
    setup_logging()