# ********** WARNING **********
# This file is designed to wipe
# the database - USE CAUTIOUSLY
# *****************************

# This script has some rough edges - if they bother you, fix them.

import psycopg2
import yaml

print("Please select a database (dev or prod):")

# pYtHoN dOEsN'T nE3D y0u To dEfiNe VarIaBLes... Unless you want your code to work you daft punk
dbName = "foo"

# Add used db instances here
while (dbName != "dev" and dbName != "prod"):
  dbName = input()

# Get database credentials from file because "yOu'Re nOt sUpPOsEd To pUT TheM oN tHe InTErnET"
#credFile = r'C:\Users\benjamin.pieplow\code\LighterFluid\data\profiles'
confFile = r'./config.yaml'
with open(confFile) as yaml_file:       # NOTE: For Windows, add this after credfile: ", encoding='utf-16'"
    config = yaml.safe_load(yaml_file.read())
username = config['username']
password = config['password']
dbServer = config['dbServer']

# Create a database connection to use
#dbinfo = "dbname='postgres' user='" + username + "' host='10.21.32.26' password='" + password + "'"
dbinfo = "dbname='" + dbName + "' user='" + username + "' host='" + dbServer + "' password='" + password + "'"
print(dbinfo)
conn = psycopg2.connect(dbinfo)

# Create a cursor to execute commands
cur = conn.cursor()

# Delete old data
print("Scrubbing...")
cur.execute("""DROP TABLE IF EXISTS tblProfiles CASCADE""")
cur.execute("""DROP TABLE IF EXISTS tblPhotos CASCADE""")
cur.execute("""DROP TABLE IF EXISTS tblFaces CASCADE""")

# This may take a moment - we'll see if that becomes an issue
conn.commit()

print("Scrubbing complete.")
print("Rebuiling...")

# Create Tables
# Create tblProfiles
cur.execute("""CREATE TABLE tblProfiles (
    Profile_ID VARCHAR(32) UNIQUE NOT NULL,
    First_Name VARCHAR(64) NOT NULL,
    Gender int NOT NULL,
    Bio VARCHAR,
    Birth_Year DATE NOT NULL,
    s_number BIGINT NOT NULL,
    PRIMARY KEY (Profile_ID)
)""")

# Create tblPhotos
cur.execute("""CREATE TABLE tblPhotos (
    Photo_ID VARCHAR(72) UNIQUE NOT NULL,
    Photo_URL VARCHAR(4096) NOT NULL,
    Profile_ID VARCHAR(32) NOT NULL,
    PRIMARY KEY (Photo_ID),
    CONSTRAINT fk_Profile_ID FOREIGN KEY (Profile_ID) REFERENCES tblProfiles(Profile_ID) ON DELETE CASCADE
)""")

# Create tblFaces
cur.execute("""CREATE TABLE tblFaces (
    Face_ID VARCHAR(64) UNIQUE NOT NULL,
    Photo_ID VARCHAR(72) NOT NULL,
    face_encodings DOUBLE PRECISION[128],
    face_delta_1 DOUBLE PRECISION NOT NULL,
    face_delta_2 DOUBLE PRECISION NOT NULL,
    Face_Top INT NOT NULL,
    Face_Bottom INT NOT NULL,
    Face_Left INT NOT NULL,
    Face_Right INT NOT NULL,
    PRIMARY KEY (Face_ID),
    CONSTRAINT fk_Photo_ID FOREIGN KEY (Photo_ID) REFERENCES tblPhotos(Photo_ID) ON DELETE CASCADE
)""")

# Save new database
conn.commit()

print("Rebuild Complete")

# Clean up connection to save RAM on server
conn.close()    