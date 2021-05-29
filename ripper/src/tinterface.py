# Scrape Tinder for profiles, ram them into SQL

# psycopg2 for database connection
import psycopg2
# yaml for config file processing
import yaml
# requests for polling APIs
import requests
# time for slowing down to match the world
import time
# numpy for face_recognition BS
import numpy
# minio for S3 interface
from minio import Minio

# Import psycopg2 error handling
# from psycopg2 import OperationalError, errorcodes, errors

# Facial Scanning API
import faceprint

# Get database credentials from file because "yOu'Re nOt sUpPOsEd To pUT TheM oN tHe InTErnET"
confFile = r'./cfg/config.yaml'
with open(confFile) as yaml_file:       # NOTE: For Windows, add this after credfile: ", encoding='utf-16'"
    config = yaml.safe_load(yaml_file.read())
sql_username = config['username']
sql_password = config['password']
dbServer = config['dbServer']
dbName = config['dbName']
xAuthToken = config['xAuthToken']
s3Server = config['s3Server']

# Create a database connection to use
dbInfo = "dbname='" + dbName + "' user='" + sql_username + "' host='" + dbServer + "' password='" + sql_password + "'"
print(dbInfo)
conn = psycopg2.connect(dbInfo)

# Create a cursor to execute commands
cur = conn.cursor()

# Create a minio client to dump photos into S3
client = minio("s3.amazonaws.com", "ACCESS-KEY", "SECRET-KEY")

 #Keep track of unique profiles
processedProfiles = 0

#Don't get stuck in endless loop
iterations = 1


##### - Set Location - #####
  # LA      (US) 34.082760 -118.330095
  # Bingham (UK) 52.961130, -0.975765
#Latitude
latitude = 52.961130
#Longtitude
longtitude = -0.975765



# Everything passed to Tinder with API requests (TODO: Add faux client info to fool IDS)
headers = {
    'X-Auth-Token': xAuthToken
}

latlong = {
    'lat': latitude,
    'lon': longtitude
}


# Set Location
rLOC = requests.post('https://api.gotinder.com/user/ping', headers = headers, data = latlong)
rLOCjson = rLOC.json()

# Let things settle down
time.sleep(2)



# Do not loop indefinetely
while iterations > 0:
    print("Iteration: " + str(iterations))
    
    # Get profiles from API
    r = requests.get('https://api.gotinder.com/recs?locale=en', headers=headers)
    # Extract JSON from HTTP response
    apiJSON = r.json()

    # Iterate over every profile
    for profile in apiJSON['results']:
        print("Profile ID: " + profile['_id'])
        # Load values into variables for readability
        profileID = profile['_id']
        first_Name = profile['name']
        gender = int(profile['gender'])
        bio = str(profile['bio'])
        birth_Year = profile['birth_date']
        s_number = profile['s_number']

        # Flag gets set to false if write to database fails
        uniqueProfile = True

        # SQL Statement to add new profile to database
        profileSQL = """
        INSERT INTO tblProfiles (Profile_ID, First_Name, Gender, Bio, Birth_Year, s_number)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Consolidate profile data for readability
        profileData = (profileID, first_Name, gender, bio, birth_Year, s_number)

        # Catch SQL error indicating duplicate profile 
        try:
            cur.execute(profileSQL, profileData)
        except psycopg2.errors.UniqueViolation:     #Note: pylint does not like "psycopg2.errors.UniqueViolation", but Python does so we'll keep it
            print("Profile ID: " + profileID + " has already been scanned!")
            # SQL rejects queries after a SQL error is returned, until a rollback is performed
            conn.rollback()
            # Flag profile iteration
            uniqueProfile = False
        
        # Save any changes
        conn.commit()


        # SQL Statement to add photo to tblPhotos
        photoSQL = """
        INSERT INTO tblPhotos (Photo_ID, Photo_URL, Profile_ID)
        VALUES (%s, %s, %s)
        """

        # SQL Statement to add face scans to tblFaces
        facesSQL = """
        INSERT INTO tblFaces (face_id, photo_id, face_encodings, face_delta_1, face_delta_2, face_top, face_bottom, face_left, face_right)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """


        # Iterate through photos returned and log each one
        for photo in profile['photos']:
            print("    Scanning photo: " + photo['id'])
            photoID = photo['id']
            photoURL = photo['url']
            photoData = (photoID, photoURL, profileID)

            # Assume a photo is unique
            uniquePhoto = True

            try:
                cur.execute(photoSQL, photoData)
            except psycopg2.errors.UniqueViolation:     #Note: pylint does not like "psycopg2.errors.UniqueViolation", but Python does so we'll keep it
                print("    Photo ID: " + photoID + " has already been scanned!")
                # If photo has been seen, skip further processing
                uniquePhoto = False
                # SQL rejects queries after a SQL error is returned, until a rollback is performed
                conn.rollback()
            
            # Save any changes
            conn.commit()

            # Only scan a photo if it is new to the database
            if (uniquePhoto):
                # Get Faces in Photo
                faces = faceprint.get_faces(photoURL)
                # Don't put empty stuff in my pristine DB
                if (faces == False):
                    print("        No faces found!")
                else:
                    print("        Found " + str(len(faces)) + " face(s).")
                    for face in faces:
                        # Extract data from JSON
                        face_id = faceprint.get_face_id(faces[face]['encodings'])
                        print("        Face: " + str(face_id))
                        face_encodings = faces[face]['encodings']
                        face_top = faces[face]['top']
                        face_bottom = faces[face]['bottom']
                        face_left = faces[face]['left']
                        face_right = faces[face]['right']

                        # Calculate facial deltas
                        delta1, delta2 = faceprint.get_deltas(face_encodings)

                        # Load variable for SQL
                        facesData = (face_id, photoID, face_encodings.tolist(), delta1, delta2, face_top, face_bottom, face_left, face_right)

                        # Catch SQL error indicating duplicate face 
                        try:
                            cur.execute(facesSQL, facesData)
                        except psycopg2.errors.UniqueViolation:     #Note: pylint does not like "psycopg2.errors.UniqueViolation", but Python does so we'll keep it
                            print("Face ID: " + face_id + " has already been scanned!")
                            # SQL rejects queries after a SQL error is returned, until a rollback is performed
                            conn.rollback()
                        
                        conn.commit()


        # Reject the profile
        passurl = "https://api.gotinder.com/pass/" + profileID + "?locale=en&s_number=" + str(s_number)
        rPass = requests.get(passurl, headers)
        
        # Apply Changes for current profile
        conn.commit()

    # Decrement iterations to avoid loops
    iterations -= 1



# Clean up connection to save RAM on server
conn.close()    