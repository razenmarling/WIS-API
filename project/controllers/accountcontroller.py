"""Controller file.
   
	Author: Razen Chris Marling
	Date: Feb 04, 2018
	Project Name: Rocka Village Inventory System - API
	Description for this file: admin processes here
"""

from flask_restful import Resource
from project import api, app
from project.auth import Auth
from project.tools import Tools
from project.models.accountmodel import AccountModel

@api.route('/account')
class AccountController(Resource, Auth):
  """Admin Controller."""

  def __init__(self):
    """Inherited Variables.
  
      - self.errorcodes
      - self.parser
      - self.engine
      - self.session
      - self.timestamp
      - self.accnt_id -> for private authentication only
       
      possible errorcodes:
      - ACC00001 => MISSING REQUIRED FIELD (username, password, acc_type)
      - ACC00002 => DUPLICATE USERNAME
      - ACC00003 => INVALID ACCOUNT TYPE -> ALLOWED -> (1=ADMIN, 2=USER)
      - ACC00004 => SOMETHING WENT WRONG SAVING IS NOT COMPLETED
      - ACC00005 => SOMETHING WENT WRONG GET ACCOUNT IS NOT COMPLETED
    """
    Auth.__init__(self, 'private')

  def get(self):
    """Get admin data."""
    if self.errorcodes:
      return Tools().response400(self.errorcodes, self.timestamp)
      
    args_list = [('un', str, 'args', None, 'username'),
                 ('at', int, 'args', None, 'acc_type'),
                 ('l', int, 'args', 10, 'limit'),
                 ('p', int, 'args', 1, 'page')]
                 
    for args in args_list:
      self.parser.add_argument(args[0], type=args[1], location=args[2], default=args[3], dest=args[4])
      
    # parse arguments
    self.__args = self.parser.parse_args()
    
    # Initialize Model
    # start get to database , if failed return 400 response
    model = AccountModel(self.session, self.engine)
    ret_obj, errorcodes = model.get_account(self.__args)
    if errorcodes:
      return Tools().response400(errorcodes, self.timestamp)

    return Tools().response200(ret_obj, self.timestamp)
  
  def post(self):
    """Add new admin."""
    if self.errorcodes:
      return Tools().response400(self.errorcodes, self.timestamp)
    
    args_list = [('username', str, 'json', None),
                 ('password', str, 'json', None),
                 ('accounttype', int, 'json', None)]
    
    for args in args_list:
      self.parser.add_argument(args[0], type=args[1], location=args[2], default=args[3])
    
    # parse arguments
    self.__args = self.parser.parse_args()
    
    # add account_id to args to save in database --> created_by
    self.__args['accnt_id'] = self.accnt_id

    # Initialize Model
    # start saving to database , if failed return 400 response
    model = AccountModel(self.session, self.engine)
    ret_obj, errorcodes = model.add_new_account(self.__args)
    if errorcodes:
      return Tools().response400(errorcodes, self.timestamp)
    
    return Tools().response200(ret_obj, self.timestamp, 201)

@api.route('/account/login')
class AccountControllerLogin(Resource, Auth):
  """Account login."""
  
  def __init__(self):
    """Inherited Variables.
  
      - self.errorcodes
      - self.parser
      - self.engine
      - self.session
      - self.timestamp
      - self.accnt_id -> for private authentication only
       
      possible errorcodes:
      - LOG0001 => MISSING REQUIRED FIELD (username, password)
      - LOG0002 => INVALID USERNAME OR PASSWORD
    """
    Auth.__init__(self, 'public')
  
  def post(self):
    """Account login."""
    if self.errorcodes:
      return Tools().response400(self.errorcodes, self.timestamp)
    
    args_list = [('username', str, 'json', None),
                 ('password', str, 'json', None)]
    
    for args in args_list:
      self.parser.add_argument(args[0], type=args[1], location=args[2], default=args[3])
    
    # parse arguments
    self.__args = self.parser.parse_args()
    
    # Initialize Model
    # start getting credentials to database , if failed return 400 response
    model = AccountModel(self.session, self.engine)
    ret_obj, errorcodes = model.login_account(self.__args)
    if errorcodes:
      return Tools().response400(errorcodes, self.timestamp)
    
    return Tools().response200(ret_obj, self.timestamp, 201)
