"""Main file.

  Author: Razen Chris Marling
  Date: Feb 04, 2018
  Project Name: Rocka Village Inventory System - API
  Description for this file: this is the brain of the project
"""

from sqlalchemy import create_engine
from flask import Flask
from flask_restful import Api
from .tools import Tools
import types

app = Flask(__name__, static_url_path='')
api =Api(app)
app.config.from_object('config')
api.route = types.MethodType(Tools.api_route, api)


# ===========================SET UP LOGGER==================================
Tools.initialize_logger(app.config['LOG_PATH'])
# ===============================END========================================


# =====================SET UP DATABASE IF NEEDED============================
try:
	# open connection
	engine = create_engine(app.config['CONNSTR'])
	# check if DB exist - create if not
	Tools.check_db_exist(engine)
	# check if DB tables is same with object tables
	Tools.inspect_tables(engine)
	# check if will add new column to the database
	Tools.inspect_columns(engine, app.config['DB_TYPE'])
	# close connection
	engine.dispose()
except Exception as exc:
	Tools.log(exc, err=True)
# ===============================END========================================


# ============================IMPORT RESOURCES==============================
from .controllers.accountcontroller import AccountController
from .controllers.accountcontroller import AccountControllerLogin
# ===============================END========================================
