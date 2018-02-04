"""Main file.
   
   Author: Razen Chris Marling
   Date: Feb 04, 2018
   Project Name: Rocka Village Inventory System - API
   Description for this file: this is the brain of the project
"""

from flask import Flask
from flask_restful import Api

app = Flask(__name__, static_url_path='')
api = Api(app)
app.config.from_object('config')

@app.route('/')
def index():
	return 'sample'
