from flask import Flask, json, request
import requests
#import tinder_api

# Stuff copied from flask tutorial (used to test flask features)
companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
api = Flask(__name__)
@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

# Basic informative page (used to test if service is online)
@api.route('/', methods=['GET'])
def index():
  return "Welcome to the lighterfluid tinder interface!"

@api.route('/recs', methods=['GET'])
def get_recs():
  tapi_token = request.args.get('tapi_token')
  headers = {'X-Auth-Token': tapi_token}
  recs_req = requests.get('https://api.gotinder.com/v2/recs/core?locale=en-GB', headers=headers)
  # Use: http://localhost:5000/rip?tapi_token=85d32ae5-4e57-4f50-a698-98af3b71e06c&lat=-95.651354&lon=35.638435
  return recs_req.json()


# Run the bastard
if __name__ == '__main__':
    api.run(host='0.0.0.0')
