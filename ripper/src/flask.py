# Dumped code from main, this handles the web API. #TODO

# Borrow data from Tinder's API and push it into SQL
# Depends:
from flask import Flask, json, request
import tinder_api

# Stuff copied from flask tutorial
companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
api = Flask(__name__)
@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

# Basic informative pag
@api.route('/', methods=['GET'])
def index():
  return "Welcome to the lighterfluid ripper!"

# Main profile to pull from
@api.route('/rip')
def rip():
  tapi_token = request.args.get('tapi_token')
  latitude = request.args.get('lat')
  longtitude = request.args.get('lon')
  range = request.args.get('range')

  print("tapi = " + tapi_token)

  # Set Location
#  tinder_api.set_location(tapi_token, latitude, longtitude)

  return tinder_api.get_recs(tapi_token)
