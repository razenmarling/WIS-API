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

	def __init__(self):
		"""Get Requried headers and initialize variables."""

		self.errorcodes = []
		self.__parser = reqparse.RequestParser()
		self.__required_headers = ['timestamp', 'client',
								   'authorization']
		# add arguments to parser
		for headers in self.__required_headers:
			self.__parser.add_argument(headers, location='headers')
		# get all arguments from headers and store to self.__args
		self.__args = self.__parser.parse_args()
		# check for required headers
		for index, headers in enumerate(self.__required_headers):
			if not self.__args.get(headers, None):
				self.errorcodes.append('MH000{}'.format(index + 1))
		# get client token
		client = self.__args.get('client', '')
		client_token = app.config['CLIENT'].get(client, '')
		# connect to database
		self.__connect_to_database()

	def public_auth(self):
		"""Public Authentiation.
		   
		   Authentication that don't requires a credentials.
		"""
		pub_authorization = Tools.sha1(client + client_token + timestamp)
		if self.__args['authorization'] != pub_authorization:
			self.errorcodes.append('AU0001')
		else:
			if self.__args['timestamp'] + 600 < time.time():
				self.errorcodes.append('AU0002')

	def private_auth(self):
		"""Private Authentiation.
		   
			 Authentication that requires credentials.
		"""
		retval = True


		return retval

	def __connect_to_database(self):
		"""Connect to database."""
		try:
			self.engine = create_engine(app.config['CONNSTR'])
			self.session = sessionmaker(bind=engine)
		except:
			self.errorcodes.append('DB0001')
