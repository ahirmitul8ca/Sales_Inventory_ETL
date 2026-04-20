import os
import pandas as pd
import logging
from file_manager import get_latest_export ,EXPORTS_DIR
from db_utlis import get_engine
from pathlib import Path



logger = logging.getLogger(__name__)
export_path= EXPORTS_DIR

def read_data():
    logger.info("Extracting inventory data")

    prefix="inventory_report"

    file_name=get_latest_export(prefix,export_path)

    f = export_path / file_name

    if f.exists():
        logger.info(f"reading file {f}")
        return pd.read_csv(f)
    else:
        logger.error(f"File not found: {f}")
        return None

    











    