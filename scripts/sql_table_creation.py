## Importing packages
import dbm
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

## Dropping existing tables & replace with new tables
def drop_tables_limited(dbList, db_source):
    for table in dbList:
        if table.startswith('production') == False:
            db_source.exectute(f'Drop table {table}')
            print(f'{table} has been dropped')
        else:
            print(f'{table} has not been dropped')

def drop_tables_all(dbList, db_source):
    for table in dbList:
        db_source.execute(f'Drop table {table}')
        print(f'{table} has been dropped')
    else:
        print(f'{table} has not been dropped')

## Loading credentials for connection
load_dotenv()

GCP_MYSQL_HOSTNAME = os.getenv("GCP_MYSQL_HOSTNAME")
GCP_MYSQL_USER = os.getenv("GCP_MYSQL_USERNAME")
GCP_MYSQL_PASSWORD = os.getenv("GCP_MYSQL_PASSWORD")
GCP_MYSQL_DATABASE = os.getenv("GCP_MYSQL_DATABASE")

## Creating connection string

connection_string_gcp = f'mysql+pymysql://{GCP_MYSQL_USER}:{GCP_MYSQL_PASSWORD}@{GCP_MYSQL_HOSTNAME}:3306/{GCP_MYSQL_DATABASE}'
db_gcp = create_engine(connection_string_gcp)

## Pulling database names

tableNames_gcp = db_gcp.table_names()

## Developing new tables
tableNames_gcp = ['patients', 'medications', 'treatment_procedures', 'conditions', 'social determinants']

## Deleting everything in the database
drop_tables_all(tableNames_gcp, db_gcp)


########## Creating new tables ##########

## Creating patients table
table_prod_patients = """
create table if not exists production_patients (
    id int auto_increment,
    mrn varchar(255) default null unique,
    first_name varchar(255) default null,
    last_name varchar(255) default null,
    date_of_birth date default null,
    gender varchar(255) default null,
    ssn varchar(255) default null,
    zip_code varchar(255) default null,
    contact_mobile varchar(255) default null,
    contact_email varchar(255) default null,
    PRIMARY KEY (id)
);
"""

## Creating medications table
table_prod_medications = """
create table if not exists production_medications (
    id int auto_increment,
    med_ndc varchar(255) default null,
    med_name varchar(255) default null,
    med_is_dangerous varchar(255) default null,
    PRIMARY KEY (id)
);
"""

## Creating treatment_procedures table
table_prod_treatment_procedures = """
create table if not exists production_treatment_procedures(
    id int auto_increment,
    cpt_code varchar(255) default null unique,
    cpt_name varchar(255) default null,
    PRIMARY KEY (id)
);
"""

## Creating conditions table
table_prod_conditions = """
create table if not exists production_conditions(
    id int auto_increment,
    icd10_code varchar(255) default null unique,
    icd10_description varchar(255) default null,
    PRIMARY KEY (id)
);
"""

## Creating social determinants table
table_prod_social_determinants = """
create table if not exists production_social_determinants(
    id int auto_increment,
    loinc_code varchar(255) default null unique,
    loinc_description varchar(255) default null,
    PRIMARY KEY (id)
);
"""

## Executing table creation
db_gcp.execute(table_prod_patients)
db_gcp.execute(table_prod_medications)
db_gcp.execute(table_prod_treatment_procedures)
db_gcp.execute(table_prod_conditions)
db_gcp.execute(table_prod_social_determinants)

## Pulling database names
tableNames_gcp = db_gcp.table_names()

## Dropping limited
drop_tables_limited(tableNames_gcp, db_gcp)

########## Creating new tables with foreign keys ##########

## Creating patients medication table                               ######### Requires assistance (FK)
table_prod_patients_medications = """
create table if not exists production_patients_medications (
    id int auto_increment,
    mrn varchar(255) default null,
    med_ndc varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES production_patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (med_ndc) REFERENCES production_medications(med_ndc) ON DELETE CASCADE
);
"""

## Creating patients conditions table
table_prod_patients_conditions = """
create table if not exists production_patients_conditions (
    id int auto_increment,
    mrn varchar(255) default null,
    icd10_code varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES production_patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (icd10_code) REFERENCES production_conditions(icd10_code) ON DELETE CASCADE
);
"""

## Executing table creation
db_gcp.execute(table_prod_patients_medications)
db_gcp.execute(table_prod_patients_conditions)

## Pulling database names
tableNames_gcp = db_gcp.table_names()