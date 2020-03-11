"""

  Module: api_authorization.py
  Description: 
   API authorization based on simple api-key validation to be used by the API endpoints.  
   Primary module funtion (@api_authorize) is a DECORATOR: 

  Usage: Use as a route decorator for api-methods needing immediate input validation.
  Example:
     @api_blueprint.route("/api/polygon_overlap",  methods=['POST'])
     @api_authorize
     def polygon_overlap():
     ...

  Notes: to use the same api_authorization() decorator on multiple routes you must include
         specify uniq endpoint=<endpoint> names in the route() args
 
"""
import json

## Flask modules
from functools import wraps
from flask import request, current_app


##-----------------------------------------------------------------------------------------
class ApiAuthorizationError(Exception):
  pass

##-----------------------------------------------------------------------------------------
def validate_api_key(request, d_data):
  """
    Validate API-key. Can be in payload or HEADERS
    Args:
      * d_data (dict): request payload data.
    Raises: ApiAuthorizationError if validation error.
  """
  api_key = current_app.config['API_KEY'] 
  request_api_key = None
  if 'api_key' in d_data:
    request_api_key = d_data['api_key']
  else:
    request_api_key = request.headers.get('X-Api-Key')

  if not request_api_key:
    raise ApiAuthorizationError("API request authorization failed: no api-key in payload or headers")

  if request_api_key != api_key:
    raise ApiAuthorizationError("API request authorization failed - Invalid API-Key for user (%s)" % (request_user))

##-----------------------------------------------------------------------------------------
def api_authorize(func):
  """
    Decorator function for route functions needing api-key validation.
    Expects flask.request object in JSON format from POST request. 
    Raises: ApiAuthorizationError if validation error.
  """
  @wraps(func)
  def wrapper(**kwargs):
    tag = 'api_authorize'
    ##print( "\nSTART DECORATOR: validate_payload %s" % (str(kwargs)))
    if request is None: 
      raise ApiAuthorizationError("%s: Empty request object" % (tag))
    d_payload = request.get_json(force=True) 
    ##print("PAYLOAD: %s" % str(d_payload))
    try:
      json_payload = json.dumps(d_payload)
    except Exception as e:
      raise ApiAuthorizationError("%s: Request payload is not valid json: %s" % (tag, e))
    try:
      validate_api_key(request, d_payload)
    except Exception as e:
      raise
    ret = func(**kwargs)
    ##print( "END DECORATOR: return %s\n" % (ret))
    return ret 
  return wrapper
