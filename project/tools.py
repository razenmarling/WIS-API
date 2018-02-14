"""Tools file.
   
   Author: Razen Chris Marling
   Date: Feb 04, 2018
   Project Name: Rocka Village Inventory System - API
   Description for this file: this file will hold all generic functions
"""

import hashlib
import time

class Tools(object):
  """Tools class."""

  @staticmethod
  def api_route(self, *args, **kwargs):
    # decorator for routing resource object
    def wrapper(cls):
      self.add_resource(cls, *args, **kwargs)
      return cls
    return wrapper

  @staticmethod
  def sha1(string):
    # Return a SHA1 hash of a given string
    return hashlib.sha1(string.encode('utf-8')).hexdigest()
  
  @staticmethod
  def response400(errorcodes, timestamp):
    retval = {}
    status_code = (403 if 'AU0001' in errorcodes
              or 'AU0002' in errorcodes else 400)
    retval['errorcodes'] = errorcodes
    retval['status'] = 'failed'
    res_time = timestamp - time.time()
    retval['responsetime'] = 0.001 if res_time < 0.001 else res_time
    return retval, status_code
  
  @staticmethod
  def response200(data):
    retval = {}
    status_code = 200
    
    return retval, status_code
