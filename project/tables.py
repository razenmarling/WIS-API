"""Tables file.
   
   Author: Razen Chris Marling
   Date: Feb 04, 2018
   Project Name: Rocka Village Inventory System - API
   Description for this file: ORM tables of DB
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Boolean, func, Date)
from decimal import Decimal
import datetime
import uuid

Base = declarative_base()


class GenericBase(object):
  """Generic base for response of database"""

  def as_dict(self):
      return ({c.name: getattr(self, c.name) for c in self.__table__.columns})

  def toJSON(self,*ret_fields):
      retval = {}
      tabledic = self.as_dict()
      for k in tabledic:
          if k not in ret_fields:
              continue

          if type(tabledic[k]) in [datetime.datetime,datetime.date]:
              tabledic[k] = tabledic[k].strftime('%m/%d/%Y %H:%M')
          elif type(tabledic[k]) is Decimal:
              tabledic[k] = float(tabledic[k])
          elif type(tabledic[k]) is uuid.UUID:
            tabledic[k] = str(tabledic[k])

          retval[k] = tabledic[k]

      return retval


class T_account(GenericBase, Base):
  """Admin Table."""

  __tablename__ = 'accounts'
  
  id = Column(Integer,primary_key=True)
  username = Column(String(50))
  password = Column(String(100))
  token = Column(String(100))
  acc_type = Column(Integer)
  created_by = Column(Integer)
  active = Column(Boolean)
  datecreated = Column(DateTime, default=datetime.datetime.now())
