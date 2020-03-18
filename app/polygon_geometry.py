#!/usr/bin/env python
"""

  File: polygon_geometry.py 
  Description: Simple polygon geometry methods using GeoJSON inputs
  Requires: 
    pip install shapely
    pip install geojson 
  Author: William Fanselow 2020-03-09 
  
  See tests/test_polygon_geometry.py for testing BAD json/geojson

"""
import json
import geojson
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

DEBUG = 0 ## make sure this is 0 before deploying to service 

##----------------------------------------------------------------------------------------------
class InvalidGeoJson(Exception):
  pass
 
##----------------------------------------------------------------------------------------------
def dprint(level, msg):
  """ Print debug messages """
  if level <= DEBUG:
    print("DEBUG (%d): %s" % (level, msg))

##----------------------------------------------------------------------------------------------
def basic_json_validation(obj):
  """
  Basic validation that input object is a valid json object.
  Required Arg (json|dict): GeoJSON object (we can handle json-str or dict)
  Raises: InvalidGeoJson() if object does not meet criteria for valid JSON object 
  Returns: dict representation of GeoJSON object 
  """

  d_obj = None

  ## handle "empty" objects before regular json validation: 
  ##  => '' (invalid json)
  ##  => '""' (valid json)
  ##  => {}, [], etc. (valid json)
  if not obj:
    raise InvalidGeoJson("Invalid GeoJSON format: empty object") 

  ## If input is dict, translate to json
  if isinstance(obj, dict):
    obj = json.dumps(obj)

  ## basic json validation - is obj a valid JSON object?
  try:
    d_obj = json.loads(obj)
  except TypeError as e:
    raise InvalidGeoJson("Invalid GeoJSON format: not a valid json") 
  except json.decoder.JSONDecodeError as e:
    raise InvalidGeoJson("Invalid GeoJSON format: %s" % (e)) 
  except Exception as e:
    raise 
 
  return( d_obj )
 
##----------------------------------------------------------------------------------------------
def validate_geojson_point(obj):
  """
  Validate that input object is a valid json and has valid GeoJSON format for a "Point".
  Required Arg (json|dict): GeoJSON Point object (we can handle json-str or dict)
  Raises: InvalidGeoJson() if object does not meet criteria for valid GeoJSON Point
  Returns: dict representation of GeoJSON Point 
  """

  d_point = None

  ## basic json validation
  try:
    d_point = basic_json_validation(obj)
  except Exception as e:
    raise 
  
  ## GeoJSON Point validation
  point = geojson.dumps(d_point)
  dprint(1, point)
  json_point = geojson.loads(point)
  dprint(1, json_point)

  try:
    point = geojson.Point(json_point) 
  except ValueError as e:
    raise InvalidGeoJson("Invalid GeoJSON Point: %s" % e) 
  dprint(1, point)

  valid = point.is_valid
  dprint(1, "VALID=%s" % valid)
  if not valid:
    l_errors = point.errors()
    dprint(1, "ERRORS:%s" % l_errors)
    raise InvalidGeoJson("Invalid GeoJSON Point: %s" % str(l_errors)) 

  return(d_point)
 
##----------------------------------------------------------------------------------------------
def validate_geojson_polygon(obj):
  """
  Validate that input object is a valid json and has valid GeoJSON format for a "Polygon".
  Required Arg (json|dict): GeoJSON Polygon object (we can handle json-str or dict)
  Raises: InvalidGeoJson() if object does not meet criteria for valid GeoJSON Polygon 
  Returns: dict representation of GeoJSON Polygon 
  """

  d_poly = None
  
  ## basic json validation
  try:
    d_poly = basic_json_validation(obj)
  except Exception as e:
    raise 
 
  ## GeoJSON Poly validation
  poly = geojson.dumps(d_poly)
  dprint(1, poly)
  json_poly = geojson.loads(poly)
  dprint(1, json_poly)

  try:
    poly = geojson.Polygon(json_poly) 
  except ValueError as e:
    raise InvalidGeoJson("Invalid GeoJSON Polygon: %s" % e) 
  dprint(1, poly)

  valid = poly.is_valid
  dprint(1, "VALID=%s" % valid)
  if not valid:
    l_errors = poly.errors()
    dprint(1, "ERRORS:%s" % l_errors)
    raise InvalidGeoJson("Invalid GeoJSON Polygon: %s" % str(l_errors)) 

  ## If the "coordinates" key is mispelled or missing, geojson.Polygon will automatically
  ## convert the object to {"coordinates": [], "type": "Polygon"} without errors.
  l_coordinates = poly.get('coordinates', None)
  if not l_coordinates:
    raise InvalidGeoJson("Invalid GeoJSON Point: Missing required parameter: [coordinates]") 

  return(d_poly)

##----------------------------------------------------------------------------------------------
def check_polygon_intersection(poly_1, poly_2):
  """
  Identify if two polygons intersect or not.
  Required Args (json): 2 polygons in GeoJSON format
  Return (dict): {"intersects": (0|1)} 
  """

  ## validate format and convert to dict
  try:
    d_poly_1 = validate_geojson_polygon(poly_1)
  except Exception as e:
    raise 
  try:
    d_poly_2 = validate_geojson_polygon(poly_2)
  except Exception as e:
    raise 
  
  d_response = {'intersects': 0}

  shape_1 = shape(d_poly_1)
  shape_2 = shape(d_poly_2)
  result = shape_1.intersects(shape_2) ## => True|False

  if result:
    d_response = {'intersects': 1}

  return(d_response)

##----------------------------------------------------------------------------------------------
def get_overlap_area(poly_1, poly_2):
  """
  Identify area of overlap of two polygons
  Required Args (json): 2 polygons in GeoJSON format
  Return (dict): {'overlap_area': <float>} 
  """
  
  ## validate format and convert to dict
  try:
    d_poly_1 = validate_geojson_polygon(poly_1)
  except Exception as e:
    raise 
  try:
    d_poly_2 = validate_geojson_polygon(poly_2)
  except Exception as e:
    raise 

  shape_1 = shape(d_poly_1)
  shape_2 = shape(d_poly_2)
  intersection = shape_1.intersection(shape_2)

  area = intersection.area
  d_response = {'overlap_area': area}

  return(d_response)

##----------------------------------------------------------------------------------------------
def check_point_in_polygon(**kwargs):
  """
  Identify if a point is "within" the boundry of a polygon
  Required kwargs: 
    * point (json): GeoJSON Point 
    * polygon (json): GeoJSON Polygon
  Return (dict): {'is_within': (0|1)} 
  """

  point = kwargs.get("point", None)
  poly = kwargs.get("polygon", None)
 
  ## validate format and convert to dict
  try:
    d_point = validate_geojson_point(point)
  except Exception as e:
    raise 
  try:
    d_poly = validate_geojson_polygon(poly)
  except Exception as e:
    raise 
  
  d_response = {'is_within': 0}

  shape_pt = shape(d_point)
  shape_poly = shape(d_poly)

  #print(shape_pt)
  #print(shape_poly)

  result = shape_pt.within(shape_poly) ## => True|False

  if result:
    d_response = {'is_within': 1}

  return(d_response)

##----------------------------------------------------------------------------------------------
if __name__ == '__main__':

  ##
  ## Some simple tests of the functions
  ## See /tests/test_* for more thorough testing
  ##

  ##
  ## GeoJSON strings (this are valid)
  ##
  poly1 = '{ "type": "Polygon", "coordinates": [ [ [ 100.0, 0.0 ], [ 101.0, 0.0 ], [ 101.0, 1.0 ], [ 100.0, 1.0 ], [ 100.0, 0.0 ] ] ] }'

  poly2 = '{ "type": "Polygon", "coordinates": [ [ [ 1208064.271243039052933, 624154.678377891657874 ], [ 1208064.271243039052933, 601260.978566187433898 ], [ 1231345.999865111429244, 601260.978566187433898 ], [ 1231345.999865111429244, 624154.678377891657874 ], [ 1208064.271243039052933, 624154.678377891657874 ] ] ] }'

  poly3 = '{ "type": "Polygon", "coordinates": [ [ [ 1199915.66622531437315, 633079.341016352758743 ], [ 1199915.66622531437315, 614453.958118694950826 ], [ 1219317.106743707787246, 614453.958118694950826 ], [ 1219317.106743707787246, 633079.341016352758743 ], [ 1199915.66622531437315, 633079.341016352758743 ] ] ] }'

  print("Testing intersection of two non-overlapping poly's...")
  try:
    result = check_polygon_intersection(poly1, poly2) 
    print("RESULT: %s" % (result))
  except Exception as e:
    raise 

  print("\nTesting intersection of two overlapping poly's...")
  try:
    result = check_polygon_intersection(poly2, poly3) 
    print("RESULT: %s" % (result))
  except Exception as e:
    raise 

  print("\nGetting overlap area of two non-overlapping poly's...")
  try:
    result = get_overlap_area(poly1, poly2) 
    print("RESULT: %s" % (result))
  except Exception as e:
    raise 

  print("\nGetting overlap area of two overlapping poly's...")
  try:
    result = get_overlap_area(poly2, poly3) 
    print("RESULT: %s" % (result))
  except Exception as e:
    raise 

  ## lat/long of Denver, Colorado
  pt_denver = { "type": "Point", "coordinates": [-104.94189, 39.743764] }

  with open('./data/colorado.json', 'r') as f_colorado:
    d_colorado = json.load(f_colorado)
    json_colorado = json.dumps(d_colorado)

    print("\nTesting if Denver (center-point lat/lon) is within Colorado...")
    result = check_point_in_polygon(point=pt_denver, polygon=json_colorado) 
    print("RESULT: %s" % (result))

 
    with open('./data/wyoming.json', 'r') as f_wyoming:
      d_wyoming = json.load(f_wyoming)
      json_wyoming = json.dumps(d_wyoming)

      print("\nTesting intersection of two adjecent states (colorado/wyoming)...")
      result = check_polygon_intersection(json_colorado, json_wyoming) 
      print("RESULT: %s" % (result))

      print("\nGetting overlapping area of two adjecent states (colorado/wyoming)...")
      result = get_overlap_area(json_colorado, json_wyoming) 
      print("RESULT: %s" % (result))

