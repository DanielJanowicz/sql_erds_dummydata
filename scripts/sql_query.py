import dbm
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

## Loading credentials for connection
load_dotenv()

GCP_MYSQL_HOSTNAME = os.getenv("GCP_MYSQL_HOSTNAME")
GCP_MYSQL_USER = os.getenv("GCP_MYSQL_USERNAME")
GCP_MYSQL_PASSWORD = os.getenv("GCP_MYSQL_PASSWORD")
GCP_MYSQL_DATABASE = os.getenv("GCP_MYSQL_DATABASE")

## Creating connection string

connection_string_gcp = f'mysql+pymysql://{GCP_MYSQL_USER}:{GCP_MYSQL_PASSWORD}@{GCP_MYSQL_HOSTNAME}:3306/{GCP_MYSQL_DATABASE}'
db_gcp = create_engine(connection_string_gcp)

## Creating queries
query_meds = pd.read_sql_query("SELECT * FROM patient_portal.production_medications", db_gcp)
query_treat_procedures = pd.read_sql_query("SELECT * FROM patient_portal.production_treatment_procedures", db_gcp)
query_conditions = pd.read_sql_query("SELECT * FROM patient_portal.production_conditions", db_gcp)

query_table = pd.read_sql_query("show tables", db_gcp)
query_database = pd.read_sql_query("show databases", db_gcp)
