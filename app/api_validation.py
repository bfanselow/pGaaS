"""
 
  Module: api_validation.py
  Description: 
   Very simple data validation functions to be used by the API endpoints. 
   Primary module function is DECORATOR: @api_data_validate

   !!!!!!!!!!!!!!
   This does NOT attempt to validate GeoJSON data (which will be done by polygon_geometry.py)
   It simply checks for the exists of a list of 2 or more objects in the "polygons" list.
   !!!!!!!!!!!!!!

  Usage: Use as a route decorator AFTER @api_authorize decorator. 
  Example:
     @api_blueprint.route("/api/polygon_overlap",  methods=['POST'])
     @api_authorize
     @api_data_validate
     def polygon_overlap():
     ...

  Notes: to use the same api_data_validate() decorator on multiple routes you must include
         specify uniq endpoint=<endpoint> names in the route() args
 
"""
## Flask modules
from functools import wraps
from flask import request, current_app

##-----------------------------------------------------------------------------------------
class ApiDataError(Exception):
  pass

##-----------------------------------------------------------------------------------------
def api_data_validate(func):
  """
    Decorator function for API request payload schema validation. Must be positioned AFTER @api_authorize. 
    Expects flask.request object in JSON format. 
    Raises: ApiDataError if validation error
    Return True
  """
  @wraps(func)
  def wrapper(**kwargs):
    ##print( "\nSTART DECORATOR: validate_schema %s" % (str(kwargs)))
    if request is None: 
      raise ApiDataError("Empty request object")
    d_payload = request.get_json(force=True) 
    polygons = d_payload.get('polygons', None)
    if polygons is None:
      raise ApiDataError("Request payload must contain a list of 2 or more polygons")
    if not isinstance(polygons, list): 
      raise ApiDataError("Request payload must contain a list of 2 or more polygons")
    if len(polygons) < 2:
      raise ApiDataError("Request payload must contain a list of 2 or more polygons")
 
    ret = func(**kwargs)
    ##print( "END DECORATOR: return %s\n" % (ret))
    return ret 
  return wrapper
