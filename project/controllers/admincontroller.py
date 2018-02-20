"""Controller file.
   
	Author: Razen Chris Marling
	Date: Feb 04, 2018
	Project Name: Rocka Village Inventory System - API
	Description for this file: admin processes here
"""

import uuid
from flask_restful import Resource
from project import api, app
from .authcontroller import AuthController
from project.tools import Tools
from project.models.adminmodel import AdminModel

@api.route('/admin')
class AdminController(Resource, AuthController):
  """Admin Controller."""

  def __init__(self):
    """Inherited Variables.
  
       - self.errorcodes
       - self.parser
       - self.engine
       - self.session
       - self.timestamp
    """
    AuthController.__init__(self, 'private')

  def get(self):
    """Get admin data."""
    if self.errorcodes:
      return Tools().response400(self.errorcodes, self.timestamp)

    return {'data': 'sample'}
  
  def post(self):
    """Add new admin.
      
      errorcodes:
      - ADMN00001 => DUPLICATE USERNAME
      - ADMN00002 => SOMETHING WENT WRONG SAVING IS NOT COMPLETED
    """
    if self.errorcodes:
      return Tools().response400(self.errorcodes, self.timestamp)
    
    args_list = [('username', str, 'json', None, True),
                 ('password', str, 'json', None, True)]
    
    for args in args_list:
      self.parser.add_argument(args[0], type=args[1], location=args[2], default=args[3], required=args[4])
    
    self.__args = self.parser.parse_args()
    model = AdminModel(self.session, self.engine)
    
    duplicate_test = model.check_duplicate_username(self.__args['username'])
    if not duplicate_test:
      return Tools().response400(['ADMN00001'], self.timestamp)
    
    # make username lowercase for generalization
    self.__args['username'] = self.__args['username'].lower()
    # encrypt password
    self.__args['password'] =  Tools().sha1(app.config['SALT'] + self.__args['password'].lower())
    # generate token
    self.__args['token'] = str(uuid.uuid4())
    # active is always true for new admin
    self.__args['active'] = True

    status = model.add_new_admin(self.__args)
    
    if not status:
      return Tools().response400(['ADMN00002'], self.timestamp)
    
    return Tools().response200({}, self.timestamp, 201)
