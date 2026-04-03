import pandas as pd
import logging
from db_utlis import get_engine
from datetime import datetime
import logging
import file_manager
import os
import fsystem


fsystem.init_fsys()



logger = logging.getLogger(__name__)


def extract_sales(engine):
    logger.info("Extracting sales")
    query="select * from monthly_sales_view"
    return pd.read_sql(query,engine)

def transform_Sales(df):
    logger.info(f"Transforming data {len(df)} records")

    df['Extracted_At'] =datetime.now().strftime("%Y-,%m-%d %H:%M:%S")
    logger.info(F"Transformation complete {len(df)}")

    return df

def load_to_csv(df):

    file_name=file_manager.get_daily_filename("sales_report","csv")
    filepath = os.path.join("exports",file_name)
    logger.info(f"file exported to {filepath} ")
    df.to_csv(filepath,index=False)
    logger.info("success")

    
    




def run_sales_pipleine():
    logger.info("starting pipeline")
    try:
        engine = get_engine()
        raw_data = extract_sales(engine)
        clean_data=transform_Sales(raw_data)
        load_to_csv(clean_data)




    except Exception as e:
        logger.error(f"sales pipline failed : {e}",exc_info=True)
        raise


