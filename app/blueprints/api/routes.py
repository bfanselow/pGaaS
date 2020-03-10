"""

 Route mapping for the "api" blueprint.

"""
import json

## Flask modules
from flask import Blueprint, request, current_app, jsonify

## Custom modules 
import utils
import polygon_geometry
from api_authorization import api_authorize
from api_validation import api_data_validate

## Create a blueprint object
blueprint_id = 'api'
bp_api = Blueprint(blueprint_id, __name__, template_folder="views")
setattr(bp_api, 'id', blueprint_id)

##---------------------------------------------------------------------------------------
## POST request to identify if there is an intersection between 2 polygons 
@bp_api.route("/api/polygon_intersection",  methods=['GET', 'POST'], endpoint='polygon-intersection' )
@api_authorize
@api_data_validate
def polygon_intersection():
  tag = "%s.polygon_intersection()" % blueprint_id
  d_request_data = request.get_json(force=True)
  
  l_polygons = d_request_data['polygons'] ## already validated existence
  poly_1 = l_polygons[0]
  poly_2 = l_polygons[1]
  ## TODO: should validate that user only passed in two. We are validating 2 or more, but ignoring items > 2

  #print(poly_1)
  #print(poly_2)

  d_result = {"intersection": 0} 

  result = polygon_geometry.check_polygon_intersection(poly_1, poly_2) ## => (True|False)
  if result:
    d_result["intersection"] = 1 
 
  result = jsonify(d_result)
  return(result)

##---------------------------------------------------------------------------------------
## POST request to calculate union between 2 or more polygons 
@bp_api.route("/api/polygon_union",  methods=['GET', 'POST'], endpoint='polygon-union' )
@api_authorize
@api_data_validate
def polygon_union():
  tag = "%s.polygon_union()" % blueprint_id
  d_request_data = request.get_json(force=True)

  print("%s: Getting union of polygons: %s" % (tag, str(d_request_data)))

  l_polygons = d_request_data['polygons'] ## already validated existence

  d_result = polygon_geometry.get_polygon_union(*l_polygons) ## => dict 
  result = jsonify(d_result)

  return(result)

