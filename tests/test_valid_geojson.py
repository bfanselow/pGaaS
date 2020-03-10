"""
 File: test_valid_geojson.py

 Description: pytest tests for both methods using VALID geojson objects
 
"""
import json
import pytest
from app.polygon_geometry import check_polygon_intersection, get_polygon_union

POLY_1 = '{"type": "Polygon", "coordinates": [[[ 100.0, 0.0 ], [ 101.0, 0.0 ], [ 101.0, 1.0 ], [ 100.0, 1.0 ], [ 100.0, 0.0 ]]]}'
POLY_2 = '{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }'
 
##------------------------------------------------------------------------

##------------------------------------------------------------------------
def test_polygon_intersection():
    ## Test check_polygon_intersection() with two polygons that do intersect 
    result = check_polygon_intersection(POLY_1, POLY_1) 
    assert result == True

##------------------------------------------------------------------------
def test_polygon_NON_intersection():
    ## Test check_polygon_intersection() with two polygons that do NOT intersect 
    result = check_polygon_intersection(POLY_1, POLY_2) 
    assert result == False 

##------------------------------------------------------------------------
def test_colorado_wyoming_union():
    ## Test get_polygon_union() with two adjecent state polygon objects 

    with open('./tests/colorado.json', 'r') as f_colorado:
      d_colorado = json.load(f_colorado)
      json_colorado = json.dumps(d_colorado)
 
      with open('./tests/wyoming.json', 'r') as f_wyoming:
        d_wyoming = json.load(f_wyoming)
        json_wyoming = json.dumps(d_wyoming)

      result = check_polygon_intersection(json_colorado, json_wyoming) 
      assert result == True
##------------------------------------------------------------------------
def test_colorado_montana_union():
    ## Test get_polygon_union() with two non-adjecent state polygon objects 

    with open('./tests/colorado.json', 'r') as f_colorado:
      d_colorado = json.load(f_colorado)
      json_colorado = json.dumps(d_colorado)
 
      with open('./tests/montana.json', 'r') as f_montana:
        d_montana = json.load(f_montana)
        json_montana = json.dumps(d_montana)

      result = check_polygon_intersection(json_colorado, json_montana) 
      assert result == False 


