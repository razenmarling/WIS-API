"""Tools file.
   
   Author: Razen Chris Marling
   Date: Feb 04, 2018
   Project Name: Rocka Village Inventory System - API
   Description for this file: this file will hold all generic functions
"""

import hashlib
import time
import logging
import os

from sqlalchemy import inspect
from sqlalchemy_utils.functions import database_exists, create_database
from .tables import Base

class Tools(object):
  """Tools class."""

  @staticmethod
  def api_route(self, *args, **kwargs):
    """Decorator for routing resource object."""
    def wrapper(cls):
      self.add_resource(cls, *args, **kwargs)
      return cls
    return wrapper

  @staticmethod
  def sha1(string):
    """Return a SHA1 hash of a given string."""
    return hashlib.sha1(string.encode('utf-8')).hexdigest()
  
  @staticmethod
  def response400(errorcodes, timestamp):
    """Failed response."""
    retval = {}
    status_code = (403 if 'AU0001' in errorcodes
              or 'AU0002' in errorcodes else 400)
    retval['errorcodes'] = errorcodes
    retval['status'] = 'failed'
    res_time = timestamp - time.time()
    retval['responsetime'] = 0.001 if res_time < 0.001 else res_time
    return retval, status_code
  
  @staticmethod
  def response200(data=None, timestamp=0, s_c=None):
    """Success response."""
    retval = data if data else {}
    status_code = s_c if s_c else 200
    retval['status'] = 'success'
    res_time = timestamp - time.time()
    retval['responsetime'] = 0.001 if res_time < 0.001 else res_time
    
    return retval, status_code
  
  @staticmethod
  def check_db_exist(engine):
    """Checking if DB exist."""
    res = database_exists(engine.url)
    if not res:     
      try:
        create_database(connstr)
      except Exception as exc:
        pass
      else:
        Base.metadata.create_all(engine)
        
  @staticmethod
  def inspect_tables(engine):
    """Check if will create new table on the database."""
    inspector = inspect(engine)

    # get tables base from objects in table.py
    object_tables = list(Base.metadata.tables.keys())
    
    # get tables from the database
    db_tables = list(inspector.get_table_names())

    if len(object_tables) > len(db_tables):
      # if object tables is greater than tables from DB
      # get the diff and create table on DB
      diff = list(set(object_tables) - set(db_tables))
      for _t in diff:
        Base.metadata.tables[_t].create(engine, checkfirst=True)
    elif len(object_tables) == len(db_tables):
      # if object tables is equal to tables from DB
      # check for difference from object table thats not in tables from DB
      # then create
      for _t in object_tables:
        if _t not in db_tables: Base.metadata.tables[_t].create(engine, checkfirst=True)

  @staticmethod
  def inspect_columns(engine, dialect):
    """."""
    add_commands = {
      'mysql': ['ALTER TABLE {table} ADD {col_name} {type} {nullable}',
                ',ADD CONSTRAINT fk_{fk_col} FOREIGN KEY ({fk_col}) REFERENCES {table_ref}({col_ref});'],
      'postgre': ['ALTER TABLE {table} ADD COLUMN {col_name} {type} {nullable}'
                  ',ADD CONSTRAINT fk_{fk_col} FOREIGN KEY ({fk_col}) REFERENCES {table_ref}({col_ref});'],
    }
    inspector = inspect(engine)
    tables = Base.metadata.tables
    
    # get object table column names
    object_cols = lambda table: [col.name for col in table.c]
    
    # get db table column names
    db_cols = lambda cols: [dict_val['name'] for dict_val in cols]
    
    for _t in tables:
      o_c = object_cols(tables[_t])
      d_c = db_cols(inspector.get_columns(_t))
      
      if o_c > d_c:
        diff = list(set(o_c) - set(d_c))
        
        for col_name in diff:
          cons = ''
          column = tables[_t].c[col_name]
          c_name = column.name
          c_type = column.type
          c_nullable = 'NULL' if column.nullable else 'NOT NULL'
          c_primary_key = column.primary_key
          c_foreign_key = None
          if column.foreign_keys:
            c_foreign_key = [(list(column.foreign_keys)[i].column.table.name,
                             list(column.foreign_keys)[i].column.name)
                             for i, fk in enumerate(list(column.foreign_keys))]

          stsql = add_commands[dialect][0].format(table=_t, col_name=c_name,
                                                  type=c_type, nullable=c_nullable)
          if c_foreign_key:
            cons = add_commands[dialect][1].format(fk_col=col_name, table_ref=c_foreign_key[0][0],
                                                   col_ref=c_foreign_key[0][1])
          engine.execute(stsql + ' ' + cons)

  @staticmethod
  def initialize_logger(path):
    """Logger"""
    path = path if path else 'logs/api_logs.log'
    if not os.path.exists(path):
        with open(path, 'w'): pass

    logger = logging.getLogger('apilogs')
    hdlr = logging.FileHandler(path)
    formatter = logging.Formatter(fmt='%(asctime)s || %(levelname)s || ==> %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S%p')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    Tools.logger = logger

  @staticmethod
  def log(msg, err=False):
    if err:
      Tools.logger.error(str(msg))
    else:
      Tools.logger.info(str(msg))