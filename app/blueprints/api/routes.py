"""

 Route mapping for the "api" blueprint.

"""

## Flask modules
from flask import Blueprint, request, current_app

## Custom modules 
from utils import dprint
from api_authorization import api_authorize
##from api_validation import api_data_validate

## Create a blueprint object
blueprint_id = 'api'
bp_api = Blueprint(blueprint_id, __name__, template_folder="views")
setattr(bp_api, 'id', blueprint_id)

##---------------------------------------------------------------------------------------
## Authorized POST request to retrieve (non-sensitive only) user-data from the account
## associated with requesting user (cannot access other user accounts). 
@bp_api.route("/api/polygon_union",  methods=['GET', 'POST'], endpoint='polygon-union' )
@api_authorize
def polygon_union():
  tag = "%s.polygon_union()" % blueprint_id
  d_request_data = request.get_json()
  dprint(1, "%s: Getting union of polygons..." % (tag))

  d_return = d_request_data

  return(d_return)
