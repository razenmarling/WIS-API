"""Tools file.
   
   Author: Razen Chris Marling
   Date: Feb 04, 2018
   Project Name: Rocka Village Inventory System - API
   Description for this file: this file will hold all generic functions
"""

class Tools(object):
	"""Tools class."""

	@staticmethod
	def api_route(self, *args, **kwargs):
		# decorator for routing resource object
	    def wrapper(cls):
	        self.add_resource(cls, *args, **kwargs)
	        return cls
	    return wrapper

