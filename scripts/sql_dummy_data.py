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

## Loading credentials for connection
GCP_MYSQL_HOSTNAME = os.getenv("GCP_MYSQL_HOSTNAME")
GCP_MYSQL_USER = os.getenv("GCP_MYSQL_USERNAME")
GCP_MYSQL_PASSWORD = os.getenv("GCP_MYSQL_PASSWORD")
GCP_MYSQL_DATABASE = os.getenv("GCP_MYSQL_DATABASE")

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
        'zipcode': fake.zipcode(),
        'contact_mobile': fake.phone_number(),
        'contact_email': fake.email()
    } for x in range(10)]

df_fake_patients = pd.DataFrame(fake_patients)

## Dropping puplicate MRNs
df_fake_patients.drop_duplicates(subset=['mrn'], inplace=True)

## Moving information to patients_table
insertQuery = "INSERT INTO production_patients (mrn, first_name, last_name, date_of_birth, gender, ssn, zipcode, contact_mobile, contact_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"


