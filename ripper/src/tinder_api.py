# TODO: Make this a standalone container
# This can mostly be borrowed from here:
# https://github.com/fbessez/Tinder/blob/master/tinder_api.py

import requests

def set_location():
    print("Setting location")

def get_recs(tapi_token):
    headers = {'X-Auth-Token': tapi_token}
    recs_req = requests.get('https://api.gotinder.com/v2/recs/core?locale=en-GB', headers=headers)
    # Use: aeb2ca7e-7c60-4d9b-8bee-f9f25c486a16
    return recs_req.json()