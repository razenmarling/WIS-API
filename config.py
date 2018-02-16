"""Config file.
   
	Author: Razen Chris Marling
	Date: Feb 04, 2018
	Project Name: Rocka Village Inventory System - API
	Description for this file: this file will hold all constants
"""

# use for encryption and decryption
SALT = '$2b$12$VjmN7ZenOnbb2ZWeiLhNFO'

# set dialect to use for connection string
DB_TYPE = 'mysql'

# DB name to use. if this db is not found
# it will be created automatically
DB = 'rocka'

# Sqlalchemy dbapi lists
DBAPI = {
  'mysql': 'mysql+pymysql',
  'postgre': 'postgresql+psycopg2',
  'mssql': 'mssql+pymssql',
  'oracle': 'oracle'
}

# connection string
# mysql+pymysql://{user}:{password}@{server}/{db}"
CONNSTR = "{dbapi}://{user}:{password}@{server}/{db}".format(
  dbapi = DBAPI[DB_TYPE],
	user='root',
	password='p@ssw0rd',
	server='127.0.0.1:4000',
	db = DB
)

# IP and port where the app will listen
BIND_IP = '127.0.0.1'
BIND_PORT = 5000

# for development mode set to TRUE else FALSE
DEBUG = True

# API clients
CLIENTS = {
	'web': 'b79e75a6-9bb3-4bbf-a5a7-b2874acd3102',
	'ios': '35561121-3713-4e63-94c4-6f451660128b',
	'android': '4b0869d4-fa5d-4c7f-899c-5427b5c5e9dd'
}