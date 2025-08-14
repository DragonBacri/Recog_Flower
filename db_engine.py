import os
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import  text


### --- Configuration ---
# It's best practice to load sensitive data from environment variables
# rather than hardcoding them in your source code.
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "antherosfluffydex")
REGION = os.environ.get("GCP_REGION", "us-central1")
INSTANCE_NAME = os.environ.get("GCP_INSTANCE_NAME", "antheros-fluffy-dex")
DB_USER = os.environ.get("DB_USER", "sqlserver")
DB_PASS = os.environ.get("DB_PASS", "9R>%&-:ZXl&:FBZa") # WARNING: Hardcoding passwords is a security risk!
DB_NAME = os.environ.get("DB_NAME", "Default")

# initialize parameters
project_id = "AntherosFluffyDex"
region = "us-central1-c"
instance_name = "antheros-fluffy-dex"
INSTANCE_CONNECTION_NAME = "antherosfluffydex:us-central1:antheros-fluffy-dex" # i.e demo-project:us-central1:demo-instance
DB_USER = "sqlserver"


# initialize Connector object
connector = Connector()

# function to return the database connection object
def get_engine():
    def get_conn():
        return connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pytds",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )

    # create connection pool with 'creator' argument to our connection object function
    engine = sqlalchemy.create_engine(
        "mssql+pytds://",
        creator= get_conn,
    )
    return engine

def add_pred_history(engine, pred_id, today) :
    insert_query = text("""
    INSERT INTO fact_history_predicts (flower_id, date) 
    VALUES ( :flower_id, :date_val)
    """)
    params = { 
        "flower_id": pred_id, 
        "date_val": today  # Pass the raw datetime object here
    }
    with engine.connect() as connection:
        # The transaction ensures the table creation is atomic
        with connection.begin() as transaction:
            connection.execute(insert_query,params)
