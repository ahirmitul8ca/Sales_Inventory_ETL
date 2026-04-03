import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import urllib

load_dotenv()

def get_engine():
    # 1. Load your .env variables
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    # 2. Use the "Direct Port" address since we verified 1433 is open
    server_with_port = "localhost,1433"
    
    # 3. Build the connection string
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={server_with_port};"
        f"Database={database};"
        f"UID={user};"
        f"PWD={password};"
    )

    print(f"DEBUG: Connecting directly to {server_with_port}...")
    
    quoted_conn = urllib.parse.quote_plus(conn_str)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={quoted_conn}")