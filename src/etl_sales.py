import pandas as pd
import logging
from db_utlis import get_engine
from datetime import datetime
import logging
import file_manager
import os 


logger = logging.getLogger(__name__)


def extract_sales(engine):
    logger.info("Extracting Monhlty sales data")
    query = "select * from monthly_sales_view"
    return pd.read_sql(query,engine)

def transform_sales(df):
    logger.info(f"transforming data {len(df)} records")

    # df=df[df['OrderQuantity']>1].copy()

    df['Extracted_At'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"Transforamtion Complete {len(df)}")
    return df

def load_to_csv(df):

    file_name=file_manager.get_daily_filename("sales_report","csv")
    file_path = os.path.join("exports",file_name)
    logger.info(f"file exported to  {file_path} ")

    df.to_csv(file_path,index=False)
    logger.info("susccess")


def run_sales_pipeline():
    logger.info("Starting pipleine")
    try:
        engine = get_engine()
        raw_data = extract_sales(engine)
        clean_data = transform_sales(raw_data)
        load_to_csv(clean_data)
    except Exception as e:
        logger.error(f"Sales pipline failed : {e}", exc_info=True)
        raise