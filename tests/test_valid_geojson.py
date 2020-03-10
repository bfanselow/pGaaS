"""
 File: test_valid_geojson.py

 Description: pytest tests for both methods using VALID geojson objects
 
"""

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
