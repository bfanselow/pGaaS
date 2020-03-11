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
def validate_geojson(obj):
  """
  Validate that input object is a valid json and has valid GeoJSON format for a Polygon.
  Required Arg (json|dict): polygon object in GeoJSON format (we can handle json-str or dict)
  Raises: InvalidGeoJson() if oject does not meet criteria for valid GeoJSON 
  Returns: dict representation of GeoJSON object
  """

  d_poly = None

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
    d_poly = json.loads(obj)
  except TypeError as e:
    raise InvalidGeoJson("Invalid GeoJSON format: not a valid json") 
  except json.decoder.JSONDecodeError as e:
    raise InvalidGeoJson("Invalid GeoJSON format: %s" % (e)) 
  except Exception as e:
    raise 
 
  ## GeoJSON validation
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
    raise InvalidGeoJson("Invalid GeoJSON Polygon: Empty coordinates") 

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
    d_poly_1 = validate_geojson(poly_1)
  except Exception as e:
    raise 
  try:
    d_poly_2 = validate_geojson(poly_2)
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
    d_poly_1 = validate_geojson(poly_1)
  except Exception as e:
    raise 
  try:
    d_poly_2 = validate_geojson(poly_2)
  except Exception as e:
    raise 

  shape_1 = shape(d_poly_1)
  shape_2 = shape(d_poly_2)
  intersection = shape_1.intersection(shape_2)

  area = intersection.area
  d_response = {'overlap_area': area}

  return(d_response)

##----------------------------------------------------------------------------------------------
if __name__ == '__main__':

  ##
  ## Some simple tests of the functions
  ## See /tests/test_polygon_geometry.py for testing BAD json/geojson)
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

  with open('./data/colorado.json', 'r') as f_colorado:
    d_colorado = json.load(f_colorado)
    json_colorado = json.dumps(d_colorado)
 
    with open('./data/wyoming.json', 'r') as f_wyoming:
      d_wyoming = json.load(f_wyoming)
      json_wyoming = json.dumps(d_wyoming)

      print("\nTesting intersection of two adjecent states (colorado/wyoming)...")
      result = check_polygon_intersection(json_colorado, json_wyoming) 
      print("RESULT: %s" % (result))

      print("\nGetting overlapping area of two adjecent states (colorado/wyoming)...")
      result = get_overlap_area(json_colorado, json_wyoming) 
      print("RESULT: %s" % (result))

