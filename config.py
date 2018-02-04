"""Config file.
   
   Author: Razen Chris Marling
   Date: Feb 04, 2018
   Project Name: Rocka Village Inventory System - API
   Description for this file: this file will hold all constants
"""

# use for encryption and decryption
SALT = '$2b$12$VjmN7ZenOnbb2ZWeiLhNFO'

# connection string
# mysql+pymysql://{user}:{password}@{server}/{db}"
CONNSTR = "mysql+pymysql://{user}:{password}@{server}/{db}".format(
	user='root',
	password='razen12345',
	server='127.0.0.1:3306',
	db='rocka'
)

# IP and port where the app will listen
BIND_IP = '127.0.0.1'
BIND_PORT = 5000
