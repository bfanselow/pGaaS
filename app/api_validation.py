"""
 
  Module: api_validation.py
  Description: 
   Validation functions to be used by the API endpoints.  Primary module function is DECORATOR: 
    * @api_validate():  used as a decorator for API routes needing POST payload schema validation.

  Usage: Use as a route decorator AFTER @api_authorize decorator. 
  Example:
     @api_blueprint.route("/api/polygon_union",  methods=['POST'])
     @api_authorize
     @api_data_validate
     def polygon_union():
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
def validate_schema(d_data):
  """
    Validate API schema. 
    Raises: ApiDataError if validation error
    Return True
  """
  endpoint = request.endpoint 
  capp = current_app._get_current_object()
  d_api_methods = capp.config['API_METHODS']
  d_method_config = d_api_methods.get(endpoint, None)
  if not d_method_config:
    raise ApiDataError("API request validaion failed: no method configuration for endpoint: %s" % (endpoint))
  d_schema = d_method_config.get('payload', None)
  if not d_schema:
    raise ApiDataError("API request validation failed: no schema definition for endpoint: %s" % (endpoint))
  print( "Validating schema for endpoint (%s): %s" % (endpoint, d_schema))
  
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
    d_payload = request.get_json() 
    if not d_payload:
      raise ApiDataError("Request payload is not valid json")
    try:
      validate_schema(d_payload)
    except Exception as e:
      raise
    ret = func(**kwargs)
    ##print( "END DECORATOR: return %s\n" % (ret))
    return ret 
  return wrapper
