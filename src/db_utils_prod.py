import os
import urllib
import struct
from sqlalchemy import create_engine
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    # In Prod, we pull the server address from the environment
    server = os.getenv("DB_SERVER") 
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    # Production often requires Encrypt=yes
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    # Logic for Azure AD Authentication (Common in Prod)
    if os.getenv("AUTH_MODE") == "AZURE_AD":
        credential = DefaultAzureCredential()
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("utf-16-le")
        token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
        
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
        
        @engine.event.listens_for(engine, "do_connect")
        def provide_token(dialect, conn_rec, cargs, cparams):
            cparams["attrs_before"] = {1256: token_struct}
        return engine

    # Standard SQL Auth for Production
    full_conn = conn_str + f"UID={user};PWD={password};"
    return create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(full_conn)}")