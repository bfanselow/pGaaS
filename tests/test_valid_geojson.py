"""
 File: test_valid_geojson.py

 Description: pytest tests for both methods using VALID geojson objects
 
"""
import json
import pytest
from app.polygon_geometry import check_polygon_intersection, get_overlap_area, check_point_in_polygon


POLY_1 = '{"type": "Polygon", "coordinates": [[[ 100.0, 0.0 ], [ 101.0, 0.0 ], [ 101.0, 1.0 ], [ 100.0, 1.0 ], [ 100.0, 0.0 ]]]}'
POLY_2 = '{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }'
POLY_3 = '{ "type": "Polygon", "coordinates": [[[24.950899, 60.169158], [24.953492, 60.169158], [24.953510, 60.170104], [24.950958, 60.169990], [24.950899, 60.169158]]] }'

POINT = '{ "type": "Point", "coordinates": [24.952242, 60.1696017] }'
##------------------------------------------------------------------------
INTERSECTION_TRUE  = {'intersects': 1}
INTERSECTION_FALSE  = {'intersects': 0}
IS_WITHIN_TRUE  = {'is_within': 1}
IS_WITHIN_FALSE  = {'is_within': 0}
##------------------------------------------------------------------------
def test_polygon_intersection():
    ## Test check_polygon_intersection() with two polygons that do intersect 
    result = check_polygon_intersection(POLY_1, POLY_1) 
    assert (result == INTERSECTION_TRUE) == True

##------------------------------------------------------------------------
def test_polygon_NON_intersection():
    ## Test check_polygon_intersection() with two polygons that do NOT intersect 
    result = check_polygon_intersection(POLY_1, POLY_2) 
    assert (result == INTERSECTION_FALSE) == True

##------------------------------------------------------------------------
def test_colorado_wyoming_overlap_area():
    ## Test get_overlap_area() with two adjecent state polygon objects 

    with open('./data/colorado.json', 'r') as f_colorado:
      d_colorado = json.load(f_colorado)
      json_colorado = json.dumps(d_colorado)
 
      with open('./data/wyoming.json', 'r') as f_wyoming:
        d_wyoming = json.load(f_wyoming)
        json_wyoming = json.dumps(d_wyoming)

      result = check_polygon_intersection(json_colorado, json_wyoming) 
      assert (result == INTERSECTION_TRUE) == True
##------------------------------------------------------------------------
def test_colorado_montana_overlap_area():
    ## Test get_overlap_area() with two non-adjecent state polygon objects 

    with open('./data/colorado.json', 'r') as f_colorado:
      d_colorado = json.load(f_colorado)
      json_colorado = json.dumps(d_colorado)
 
      with open('./data/montana.json', 'r') as f_montana:
        d_montana = json.load(f_montana)
        json_montana = json.dumps(d_montana)

      result = check_polygon_intersection(json_colorado, json_montana) 
      assert (result == INTERSECTION_FALSE) == True
##------------------------------------------------------------------------
def test_point_in_polygon_true():
    ## Test point_in_polygon() for True case 
    result = check_point_in_polygon(point=POINT, polygon=POLY_3) 
    assert (result == IS_WITHIN_TRUE) == True

##------------------------------------------------------------------------
def test_point_in_polygon_false():
    ## Test point_in_polygon() for False case 
    result = check_point_in_polygon(point=POINT, polygon=POLY_2) 
    assert (result == IS_WITHIN_FALSE) == True

