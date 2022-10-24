# MYSQL on GCP connected through Python and SQL Workbench

## Scripts folder:
# sql_table_creation.py
This python file connects to mySQL on a SQL server hosted on GCP.  It uses automation of queries to develop several tables pertaining to a paient portal.  

# sql_dummy_data.py
This python file also connects to mySQL, and hosts the code for creating fake patient data and uploading it to the SQL server.  This file also includes uploading real medical codes such as ICD10, LOINC, and NDC to be utilized in the database.

## Documentation folder:
# sql_query.md
This markdown file displays the several queries as well as the ERD of the database structure.  

# setup.md
This file explains the initial setup of how to connect to the SQL server and initial setup.

# resources.md
This is just another markdown file that houses the resources used in this repo. This is primarily meant to refer back to in the future, or others can utilize it for their own repo.

## Other folders/files:
- Errors (Displays errors within the repo (if applicable))
- Images (Holds images used across all markdown files(excluding errors))