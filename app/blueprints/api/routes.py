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

##
## Payload validaiton is performed by jsonschema. The jsonschema objects below are passed to the 
## @api_data_validation decorator. However, this only validates the top-level json keys and the
## associated value-types.  Deeper validation of the GeoJSON objects will be done within 
## app/polygon_geometry module.
##
json_schema_uri = 'http://json-schema.org/draft-04/schema#'

## jsonschema for point-in-polygon method (expect one point, and one polygon)
d_schema_pip = {'$schema': json_schema_uri, 'title': 'apiPostData', 'description': 'top-level payload data for point-in-polygon method', 'type': 'object', 'properties': {'point':{'type': 'object'}, 'polygon': {'type':'object'}}, 'required': ['point', 'polygon' ] }

## jsonschema for polygon-intersection or overlap methods (expect two polygons)
d_schema_2poly = {'$schema': json_schema_uri, 'title': 'apiPostData', 'description': 'top-level payload data for polygon intersect or overlap methods', 'type': 'object', 'properties': {'polygons':{'type': 'array', 'minItems': 2, 'maxItems': 2, 'items': {'type':'object'}, 'error':'Two GeoJSON objects required',  'additionalItems': False }},  'required': ['polygons']}


##---------------------------------------------------------------------------------------
## POST request to identify if there is an intersection between 2 polygons 
@bp_api.route("/api/polygon_intersection",  methods=['GET', 'POST'], endpoint='polygon-intersection' )
@api_authorize
@api_data_validate(d_schema_2poly)
def polygon_intersection():
  tag = "%s.polygon_intersection()" % blueprint_id
  d_request_data = request.get_json(force=True)
  
  #print("%s: Getting intersection of polygons: %s" % (tag, str(d_request_data)))
  
  l_polygons = d_request_data['polygons'] ## already validated existence
  poly_1 = l_polygons[0]
  poly_2 = l_polygons[1]

  #print(poly_1)
  #print(poly_2)

  d_result = polygon_geometry.check_polygon_intersection(poly_1, poly_2) ## => dict
 
  result = jsonify(d_result)
  return(result)

##---------------------------------------------------------------------------------------
## POST request to calculate overlap area between 2 polygons 
@bp_api.route("/api/polygon_overlap_area",  methods=['GET', 'POST'], endpoint='polygon-overlap' )
@api_authorize
@api_data_validate(d_schema_2poly)
def polygon_overlap_area():
  tag = "%s.polygon_overlap_area()" % blueprint_id
  d_request_data = request.get_json(force=True)

  #print("%s: Getting overlap-area of polygons: %s" % (tag, str(d_request_data)))

  l_polygons = d_request_data['polygons'] ## already validated existence
  poly_1 = l_polygons[0]
  poly_2 = l_polygons[1]

  d_result = polygon_geometry.get_overlap_area(poly_1, poly_2) ## => dict 
  result = jsonify(d_result)

  return(result)

##---------------------------------------------------------------------------------------
## POST request to identify if point is "within" a polygon
@bp_api.route("/api/point_in_polygon",  methods=['GET', 'POST'], endpoint='point-in-polygon' )
@api_authorize
@api_data_validate(d_schema_pip)
def point_in_polygon():
  tag = "%s.point_in_polygon()" % blueprint_id
  d_request_data = request.get_json(force=True)

  print("%s: Identifying if point is within polygon: %s" % (tag, str(d_request_data)))

  point = d_request_data['point']     ## already validated existence
  polygon = d_request_data['polygon'] ## already validated existence

  d_result = polygon_geometry.check_point_in_polygon(point=point, polygon=polygon) ## => dict 
  result = jsonify(d_result)

  return(result)

