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




# Get database credentials from file because "yOu'Re nOt sUpPOsEd To pUT TheM oN tHe InTErnET"
credFile = r'./userpass.json'
with open(credFile) as json_file:
    userPassJson = json.loads(json_file.read())
sql_username = userPassJson['sql_username']
sql_password = userPassJson['sql_password']


if __name__ == '__main__':
    api.run(host='0.0.0.0')
