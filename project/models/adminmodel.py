"""Model file.
   
	Author: Razen Chris Marling
	Date: Feb 04, 2018
	Project Name: Rocka Village Inventory System - API
	Description for this file: admin database processes here
"""

from project.tools import Tools
from project.tables import T_admin


class AdminModel(object):
  """Admin Model."""
  
  def __init__(self, session, engine):
    """Initialize DB connections."""
    self.__session = session
    self.__engin = engine
  
  def check_duplicate_username(self, username):
    """Check if username is already used"""
    status = True
    uname =  username.lower()

    result = self.__session.query(T_admin).filter(T_admin.username == uname).first()
    if result:
      status = False
    
    return status
  
  def add_new_admin(self, data):
    """Add new admin to database."""
    status = True
    table = T_admin()
    
    try:
      for key, value in data.items():
        setattr(table, key, value)
      self.__session.add(table)
    except Exception as exc:
      Tools.log(exc, err=True)
      status = False
    else:
      self.__session.commit()
    
    return status
