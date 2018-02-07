"""Run file.
   
  Author: Razen Chris Marling
  Date: Feb 04, 2018
  Project Name: Rocka Village Inventory System - API
  Description for this file: this is the heart of the project
"""

from project import app

if __name__ == '__main__':
  app.run(host=app.config['BIND_IP'],port=app.config['BIND_PORT'],debug=app.config['DEBUG'])