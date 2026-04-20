import os
import logging
import shutil
from datetime import datetime

logger = logging.getLogger(__name__)

LOGS_DIR = os.getenv("HOST_LOGS_PATH", "/app/logs")
EXPORTS_DIR = os.getenv("HOST_EXPORTS_PATH", "/app/exports")
DATA_DIR = os.getenv("HOST_DATA_PATH", "/app/data")
Archive_DIR = os.getenv("HOST_ARCHIVE_PATH", "/app/archive")


def ensure_directories(dir_list=None):
    """
    Creates necessary folders if they don't exist.
    Default: logs and exports.
    """
    if dir_list is None:
        dir_list = [LOGS_DIR, EXPORTS_DIR, DATA_DIR,Archive_DIR]
    
    for directory in dir_list:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Directory Created: {directory}")
        else:
            logger.debug(f"Directory already exists: {directory}")

def get_daily_filename(prefix, extension="csv"):
    """
    Generates a filename like: sales_2026-04-01.csv
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{prefix}_{today}.{extension}"

def list_exports():
    """Returns a list of all files in the exports folder."""
    
    if os.path.exists(EXPORTS_DIR):
        return os.listdir(EXPORTS_DIR)
    return []

def archive_old_file(filename, folder):
    """
    Moves a file to an 'archive' subfolder to keep your 
    main export folder clean.
    """

    target_folder = folder if folder else EXPORTS_DIR

    archive_path = Archive_DIR
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    
    source = os.path.join(target_folder, filename)
    destination = os.path.join(archive_path, filename)
    
    if os.path.exists(source):
        shutil.move(source, destination)
        logger.info(f"Archived: {filename} moved to {archive_path}")


def get_latest_export(prefix,folder):
    # Find all files in exports starting with the prefix
    files = list(folder.glob(f"{prefix}*.csv"))
    
    if not files:
        logger.warning(f"No files found with prefix: {prefix}")
        return None
    
    # Sort by creation time and take the last one
    latest_file = max(files, key=lambda x: x.stat().st_ctime)
    return latest_file
