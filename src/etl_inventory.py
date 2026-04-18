import pandas as pd
import logging

from sqlalchemy import engine
from db_utlis import get_engine
from datetime import date, datetime
import logging
import file_manager
import os


logger = logging.getLogger(__name__)

def get_data(engine,date):
    logger.info("Extracting inventory data")

    
    query = "EXEC SP_Stock_View @i_date = ?"
    # Pass it as a tuple (note the comma!)
    df = pd.read_sql(query, engine, params=(date,))
    
    return  df

def transform_inventory(df):

        logger.info(f"transforming data {len(df)} records")
        df['Extracted_At'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
        logger.info(f"Transforamtion Complete {len(df)}")



        return df


def load_to_csv(df):
    file_name=file_manager.get_daily_filename("inventory_report","csv")
    file_path = os.path.join("exports",file_name)
    logger.info(f"file exported to  {file_path} ")

    df.to_csv(file_path,index=False)
    logger.info("susccess")


def run_inventory_pipeline(date):
    logger.info("Starting inventory pipeline")
    try:
        engine = get_engine()
        raw_data=get_data(engine,date)
        clean_data=transform_inventory(raw_data)
        load_to_csv(clean_data)



    except Exception as e:
        logger.error(f"Inventory pipeline failed : {e}", exc_info=True)
        raise