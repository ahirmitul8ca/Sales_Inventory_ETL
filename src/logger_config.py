import logging
import os
from datetime import datetime
from file_manager import LOGS_DIR

def setup_logging():
    
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    # Date-only timestamp (e.g., 2026-04-01)
    today = datetime.now().strftime("%Y-%m-%d")
    log_name = f"etl_{today}.log"
    log_path = os.path.join(LOGS_DIR, log_name)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # 'mode=a' ensures multiple runs today APPEND to the same file
            logging.FileHandler(log_path, mode='a'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)