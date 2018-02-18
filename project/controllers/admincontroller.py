"""Controller file.
   
	Author: Razen Chris Marling
	Date: Feb 04, 2018
	Project Name: Rocka Village Inventory System - API
	Description for this file: admin processes here
"""

from flask_restful import Resource
from project import api
from .authcontroller import AuthController
from project.tools import Tools

@api.route('/admin')
class AdminController(Resource, AuthController):
  def __init__(self):
    AuthController.__init__(self, 'private')

  def get(self):
    if self.errorcodes:
      return Tools().response400(self.errorcodes, self.timestamp)

    return {'data': 'sample'}
