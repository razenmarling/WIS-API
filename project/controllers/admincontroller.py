"""Controller file.
   
	Author: Razen Chris Marling
	Date: Feb 04, 2018
	Project Name: Rocka Village Inventory System - API
	Description for this file: admin processes here
"""

from flask_restful import Resource
from project import api
from .authcontroller import AuthController

@api.route('/admin')
class AdminController(Resource):

	def get(self):
		return {'data': 'sample'}
