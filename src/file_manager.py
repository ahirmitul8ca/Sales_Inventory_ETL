import os
import logging
import shutil
from datetime import datetime

logger = logging.getLogger(__name__)

def ensure_directories(dir_list=None):
    """
    Creates necessary folders if they don't exist.
    Default: logs and exports.
    """
    if dir_list is None:
        dir_list = ['logs', 'exports', 'data']
    
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
    export_dir = 'exports'
    if os.path.exists(export_dir):
        return os.listdir(export_dir)
    return []

def archive_old_file(filename, folder='exports'):
    """
    Moves a file to an 'archive' subfolder to keep your 
    main export folder clean.
    """
    archive_path = os.path.join(folder, 'archive')
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    
    source = os.path.join(folder, filename)
    destination = os.path.join(archive_path, filename)
    
    if os.path.exists(source):
        shutil.move(source, destination)
        logger.info(f"Archived: {filename} moved to {archive_path}")