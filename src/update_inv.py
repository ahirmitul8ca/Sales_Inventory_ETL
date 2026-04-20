from datetime import datetime
import os
import pandas as pd
import logging
from file_manager import get_latest_export ,EXPORTS_DIR
from db_utlis import get_engine
from pathlib import Path
import fsystem
from sqlalchemy import text


logger = logging.getLogger(__name__)
export_path= Path(EXPORTS_DIR)

def read_data():
    logger.info("Extracting inventory data")

    prefix="inventory_report"

    file_name=get_latest_export(prefix,export_path)

    if file_name is None:
        logger.error(f"No file starting with '{prefix}' found in {export_path}")
        return None  # Stop right here and return to main

    else: 

        f = export_path / file_name
        print(f)

        if f.exists():
            logger.info(f"reading file {f}")
            return pd.read_csv(f)
        else:
            logger.error(f"File not found: {f}")
            return None

    
def update_inventory(df):
    
    if df is None: return
    
    engine = get_engine()

    stg = "staging_inventory"
    target = 'tbl_stock'
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    try:
        logger.info(f"uploading staging table: {stg}")
        df.to_sql(stg,engine,if_exists="replace", index=False)

        mq = f""" 
        MERGE INTO {target} AS t
        USING {stg} AS s
        ON t.S_ProductKey = s.ProductKey AND t.S_Date = s.Inv_date
        
        WHEN MATCHED THEN
            UPDATE SET 
                t.Qty = s.Stock_on_date,
                t.modified_Date = '{current_date_time}'
        
        WHEN NOT MATCHED THEN
            INSERT (S_Date, S_ProductKey, Qty, modified_Date)
            VALUES (s.Inv_date, s.ProductKey, s.Stock_on_date, '{current_date_time}');
        """


        with engine.begin() as conn:
            conn.execute(text(mq))
            logger.info(f"upsert complte for {target}")

    
    except Exception as e:
        logger.info(f"failed to upsert data: {e}")



if __name__ == "__main__":
    fsystem.init_fsys()
    logger.info("Starting inventory update process directly")
    
    df = read_data()
    print(df)
    # --- ADD THIS LOGIC ---
    if df is not None:
        logger.info(f"Successfully extracted {len(df)} rows. Starting upload...")
        update_inventory(df)
    else:
        logger.error("ETL Aborted: No data was returned from read_data().")
    # ----------------------







    