"""Controller file.
   
  Author: Razen Chris Marling
  Date: Feb 04, 2018
  Project Name: Rocka Village Inventory System - API
  Description for this file: API authentications.
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time

from flask_restful import reqparse
from project import app
from project.tools import Tools

class AuthController(object):
  """Authentications."""

  def __init__(self, authtype):
    """Get Requried headers and initialize variables.
      
       Global Parameters:
       - self.errorcodes
       - self.parser
       - self.engine
       - self.session
       - self.timestamp
    """
    self.errorcodes = []
    self.parser = reqparse.RequestParser()
    # set required headers
    self.__required_headers = [('timestamp', 0), ('client', ''),
                               ('authorization', '')]
    # add arguments to parser
    for headers in self.__required_headers:
      self.parser.add_argument(headers[0], location='headers', default=headers[1])
    # get all arguments from headers and store to self.__args
    self.__args = self.parser.parse_args()
    # get timestamp
    self.timestamp = int(self.__args.get('timestamp', 0))
    # check for required headers
    for index, headers in enumerate(self.__required_headers):
      if not self.__args.get(headers, None):
        self.errorcodes.append('MH000{}'.format(index + 1))
    # get client token
    self.__client = self.__args.get('client', '')
    self.__client_token = app.config['CLIENTS'].get(self.__client, '')
    # connect to database
    self.__connect_to_database()
    # check which authtype will use
    auth_types = {
      'public': self.__public_auth,
      'private': self.__private_auth
    }
    auth_types[authtype]()

  def __public_auth(self):
    """Public Authentiation.
       
       Authentication that don't requires a credentials.
    """
    pub_authorization = Tools.sha1(self.__client + self.__client_token + str(self.__args['timestamp']))
    if self.__args['authorization'] != pub_authorization:
      self.errorcodes.append('AU0001')
    else:
      if int(self.__args['timestamp']) + 600 < int(time.time()):
        self.errorcodes.append('AU0002')

  def __private_auth(self):
    """Private Authentiation.
       
       Authentication that requires credentials.
    """
    priv_authorization = Tools.sha1(self.__client + self.__client_token + str(self.__args['timestamp']))
    if self.__args['authorization'] != priv_authorization:
      self.errorcodes.append('AU0001')
    else:
      if int(self.__args['timestamp']) + 600 < int(time.time()):
        self.errorcodes.append('AU0002')

  def __connect_to_database(self):
    """Connect to database."""
    try:
      self.engine = create_engine(app.config['CONNSTR'])
      self.engine.connect()
      self.session = sessionmaker(bind=self.engine)()
    except Exception as exc:
      Tools.log(exc, err=True)
      self.errorcodes.append('DB0001')
