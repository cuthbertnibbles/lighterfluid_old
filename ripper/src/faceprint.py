# Call-able version of scanner for inline use
# Accepts a URL and returns a dict of faces in the image (or false if none are detected)
# Basically a web-enabled wrapper for face_recognition


import numpy as np
import face_recognition
import requests
import hashlib

from PIL import Image, ImageDraw
from io import BytesIO

import struct

def _fetch(URL):
    r = requests.get(URL)
    
    if (r.ok):
        img = Image.open(BytesIO(r.content))
        return img
    else:
        print("Error accessing image!")
        return False

# Accept a photo file location and return a dict of faces & face data in the photo
def _scan_photo(image):

    # Convert PIL Jpeg to NP Array
    image = np.array(image.convert('RGB'))

    # Create an empty dict for scanned faces
    faces = {}
    # Counter for face array
    face_num = 0

    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="hog")
    face_encodings = face_recognition.api.face_encodings(image, face_locations)

    
    for face in zip(face_locations, face_encodings):
        # Convert encodings from np.ndarray to list (for json serialization)
#        encodings_list = face[1].tolist()
        # Add face to dict
#        faces[face_num] = {"top" : face[0][0], "left" : face[0][1], "right" : face[0][2], "bottom" : face[0][3], "encodings" : encodings_list}
        faces[face_num] = {"top" : face[0][0], "left" : face[0][1], "right" : face[0][2], "bottom" : face[0][3], "encodings" : face[1]}


        # Increment array counter
        face_num = face_num + 1
    if (faces):
        return faces
    else:
        return False

def get_face_id(face_encodings):
    encodings_bytes = struct.pack('%sf' % len(face_encodings), *face_encodings)
    return hashlib.sha256(encodings_bytes).hexdigest()

def get_faces(URL):
    image = _fetch(URL)
    if (image == False):
        print("Image Capture failed! Returning False.")
        return False
    else:
        return(_scan_photo(image))

# Returns input face distance from delta referrence faces as two doubles
def get_deltas(face_encodings):

    ##### - Set facial delta markers - #####

    # Note: We could use "0.25" and "-0.25", but numpy likes arrays and I can afford the extra 2KB of RAM

    # Init arrays in RAM
    delta1_ref = np.empty(128)
    delta2_ref = np.empty(128)

    # Makes pylint happy
    i = 0
    # Create delta array waypoints (using a while loop because Python is not a real programming language)
    while i < 128:
        delta1_ref[i] = 0.25
        delta2_ref[i] = -0.25
        i+=1
    
    delta1 = np.linalg.norm([face_encodings] - delta1_ref, axis=1)
    delta2 = np.linalg.norm([face_encodings] - delta2_ref, axis=1)

    return delta1[0], delta2[0]


# Test
#output = fetch("https://images-ssl.gotinder.com/5f3d91e18cfdc10100e4d4f7/original_6016b8f1-d4b7-4c33-96b5-dd19ac838c94.jpeg")
