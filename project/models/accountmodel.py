"""Model file.
   
	Author: Razen Chris Marling
	Date: Feb 04, 2018
	Project Name: Rocka Village Inventory System - API
	Description for this file: admin database processes here
"""

from project import app
from project.tools import Tools
from project.tables import T_account

import uuid


class AccountModel(object):
  """Admin Model."""
  
  def __init__(self, session, engine):
    """Initialize DB connections."""
    self.__session = session
    self.__engine = engine
  
  def add_new_account(self, data):
    """Add new admin to database."""
    ret_obj = {}
    err = []
    clean_data, err = self.__validate_new_account(data)
    
    if not err:
      table = T_account()
      try:
        for key, value in clean_data.items():
          setattr(table, key, value)
        self.__session.add(table)
      except Exception as exc:
        Tools.log(exc, err=True)
        err.append('ACC00004')
      else:
        self.__session.commit()
    
    Tools.close_all_connection(self.__engine, self.__session)

    return ret_obj, err
  
  def __validate_new_account(self, data):
    """NEW ACCOUNT - Validate and sanitize datas before adding to database."""
    retval = {}
    err = []
    
    # ================= Check Required fields ==================
    req_fields = ['username', 'password', 'accounttype']
    if any([not data[f] for f in req_fields]):
      err.append('ACC00001')
    # =========================== END ==========================
    
    if not err:
      # ====================== Validations =====================
      # make username lowercase for generalization
      duplicate_test = self.__check_duplicate_username(data['username'])
      if not duplicate_test:
        err.append('ACC00002')
      
      # check if acc_type suplied is valid
      if data['accounttype'] not in (1, 2, '1', '2'):
        err.append('ACC00003')
      # =========================== END ========================
    
    if not err:
      # ====================== Sanitations =====================
      # make username lowercase for generalization
      retval['username'] = data['username'].lower()
      # encrypt password
      retval['password'] =  Tools().sha1(app.config['SALT'] + data['password'].lower())
      # generate token
      retval['token'] = str(uuid.uuid4())
      # active is always true for new admin
      retval['active'] = True
      # accounttype
      retval['acc_type'] = data['accounttype']
      # created by
      retval['created_by'] = data['accnt_id']
      # =========================== END ========================
    
    return retval, err
    
  def __check_duplicate_username(self, username):
    """NEW ACCOUNT - Check if username is already used."""
    status = True
    uname =  username.lower()

    result = self.__session.query(T_account).filter(T_account.username == uname).first()
    if result:
      status = False
    
    return status
  
  def login_account(self, data):
    """Get login credentials."""
    ret_obj = {}
    err = []

    req_fields = ['username', 'password']
    if any([not data[f] for f in req_fields]):
      err.append('LOG00001')
    
    if not err:
      uname = data['username']
      pwrd = Tools().sha1(app.config['SALT'] + data['password'].lower())

      result = self.__session.query(T_account).filter(T_account.username == uname).first()
      
      if result:
        if result.password == pwrd:
          ret_obj['token'] = result.token
          ret_obj['id'] = result.id
          ret_obj['username'] = result.username
          ret_obj['accounttype'] = result.acc_type
        else:
          err.append('LOG00002')
      else:
        err.append('LOG00002')
    
    Tools.close_all_connection(self.__engine, self.__session)
    
    return ret_obj, err
  
  def get_account(self, data):
    """Get list of accounts."""
    ret_obj = []
    err = []
    allowed_param = ['username', 'acc_type']
    ret_columns = ['username', 'created_by', 'datecreated',
                   'acc_type', 'active']
    search_filter = []
    
    for key in allowed_param:
      if data.get(key) not in (None, ''):
        search_filter.append(getattr(T_account, key) == data[key])
    
    offset = Tools.pagination(data['limit'], data['page'])
    
    try:
      if search_filter:
        result = self.__session.query(T_account).filter(
          *search_filter).order_by(
            T_account.id).limit(data['limit']).offset(offset).all()
      
      else:
        result = self.__session.query(T_account).order_by(
            T_account.id).limit(data['limit']).offset(offset).all()
    except Exception as exc:
      Tools.log(exc, err=True)
      err.append('ACC00005')    
    else:   
      for d in result:
        r = d.toJSON(*ret_columns)
        ret_obj.append(r)
    
    Tools.close_all_connection(self.__engine, self.__session)
    
    return ret_obj, err
