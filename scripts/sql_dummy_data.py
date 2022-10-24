## Importing packages
import dbm
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from faker import Faker
import uuid
import random
from dotenv import load_dotenv

## Loading credentials for connection
load_dotenv()

GCP_MYSQL_HOSTNAME = os.getenv("GCP_MYSQL_HOSTNAME")
GCP_MYSQL_USER = os.getenv("GCP_MYSQL_USERNAME")
GCP_MYSQL_PASSWORD = os.getenv("GCP_MYSQL_PASSWORD")
GCP_MYSQL_DATABASE = os.getenv("GCP_MYSQL_DATABASE")

## Creating connection string

connection_string_gcp = f'mysql+pymysql://{GCP_MYSQL_USER}:{GCP_MYSQL_PASSWORD}@{GCP_MYSQL_HOSTNAME}:3306/{GCP_MYSQL_DATABASE}'
db_gcp = create_engine(connection_string_gcp)

## Show databases
print(db_gcp.table_names())

## Creating fake patients data
fake = Faker()

fake_patients = [
    {
        'mrn': str(uuid.uuid4())[:8],
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_birth': fake.date_of_birth(),
        'gender': fake.random_element(elements=('M', 'F')),
        'ssn': fake.ssn(),
        'zip_code': fake.zipcode(),
        'contact_mobile': fake.phone_number(),
        'contact_email': fake.email()
    } for x in range(100)]

df_fake_patients = pd.DataFrame(fake_patients)

## Dropping puplicate MRNs
df_fake_patients.drop_duplicates(subset=['mrn'], inplace=True)

## Moving information to patients_table
insertQuery = "INSERT INTO production_patients (mrn, first_name, last_name, date_of_birth, gender, ssn, zip_code, contact_mobile, contact_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

for index, row in df_fake_patients.iterrows():
    db_gcp.execute(insertQuery, (row['mrn'], row['first_name'], row['last_name'], row['date_of_birth'], row['gender'], row['ssn'], row['zip_code'], row['contact_mobile'], row['contact_email']))
    print("Inserting row: ", index)

## Checking patients table
df_gcp = pd.read_sql_query("SELECT * FROM production_patients", db_gcp)
