
import psycopg2
import yaml

# Get database credentials from file because "yOu'Re nOt sUpPOsEd To pUT TheM oN tHe InTErnET"
#credFile = r'C:\Users\benjamin.pieplow\code\LighterFluid\data\profiles'
confFile = r'./cfg/config.yaml'
with open(confFile) as yaml_file:       # NOTE: For Windows, add this after credfile: ", encoding='utf-16'"
    config = yaml.safe_load(yaml_file.read())
sql_username = config['username']
sql_password = config['password']
dbServer = config['dbServer']

# Create a database connection to use
#dbinfo = "dbname='postgres' user='" + username + "' host='10.21.32.26' password='" + password + "'"
dbinfo = "dbname='" + dbName + "' user='" + username + "' host='" + dbServer + "' password='" + password + "'"
print(dbinfo)
conn = psycopg2.connect(dbinfo)


if __name__ == '__main__':
    api.run(host='0.0.0.0')
