import pandas as pd

def load_and_clean(path):
    # Industry Standard: Use parquet for cloud performance
    df = pd.read_parquet(path)
    return df.dropna().reset_index(drop=True)