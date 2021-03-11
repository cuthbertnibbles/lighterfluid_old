# TODO: Make this a standalone container
# This can mostly be borrowed from here:
# https://github.com/fbessez/Tinder/blob/master/tinder_api.py

import requests

def set_location(tapi_token, lat, lon):
    print("Setting location")
    headers = {'X-Auth-Token': tapi_token}
    data = {'lat': lat, 'lon': lon}
    loc_req = requests.post('https://api.gotinder.com/user/ping', headers = headers, data = data)
    return loc_req.json()



def get_recs(tapi_token):
    headers = {'X-Auth-Token': tapi_token}
    recs_req = requests.get('https://api.gotinder.com/v2/recs/core?locale=en-GB', headers=headers)
    # Use: http://localhost:5000/rip?tapi_token=85d32ae5-4e57-4f50-a698-98af3b71e06c&lat=-95.651354&lon=35.638435
    return recs_req.json()