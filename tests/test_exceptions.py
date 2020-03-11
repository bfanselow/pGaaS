"""
 File: test_exceptions.py
 Description: Testing methods for exception handling of INVALID json or geojson inputs
"""

import pytest
from app.polygon_geometry import check_polygon_intersection, get_overlap_area, InvalidGeoJson

POLY_GOOD = '{"type": "Polygon", "coordinates": [[[ 100.0, 0.0 ], [ 101.0, 0.0 ], [ 101.0, 1.0 ], [ 100.0, 1.0 ], [ 100.0, 0.0 ]]]}'
POLY_GOOD_2 = '{"type": "Polygon", "coordinates": [[[ 100.0, 2.0 ], [ 101.0, 2.0 ], [ 101.0, 5.0 ], [ 100.0, 5.0 ], [ 100.0, 0.0 ]]]}'
 
## Invalid json or geojson 
NULLSTR = ''    # invalid json
ASTER = '*'     # invalid json
QUOTES = ""     # valid json, but invalid geojson 
EMPTYLIST = []  # valid json, but invalid geojson 
EMPTYDICT = {}  # valid json, but invalid geojson 

## invalid geojson ("coord" instead of "coordinate" key)
## Surprisingly, this NOT handled by obj.is_valid as geojson.Polgon automatically converts any 
## object missing the "coordinates" key to:  {"coordinates": [], "type": "Polygon"})
BAD_COORDINATES = '{ "type": "Polygon", "coord": [ [ [ 1208064, 624154 ], [ 1208064, 601260 ], [ 1231345, 601260 ], [ 1231345, 624154 ], [ 1208064, 624154 ] ] ] }'

## invalid geojson ("tipe" instaed of "type")
BAD_TYPE = '{ "tipe": "Polygon", "coordinates": [ [ [ 1208064, 624154 ], [ 1208064, 601260 ], [ 1231345, 601260 ], [ 1231345, 624154 ], [ 1208064, 624154 ] ] ] }'

## invalid json (invalid list format in first coordinate - missing comma)
BAD_COORD_LIST = '{ "type": "Polygon", "coordinates": [ [ [ 1208064 624154 ], [ 1208064, 601260 ], [ 1231345, 601260 ], [ 1231345, 624154 ], [ 1208064, 624154 ] ] ] }'

## invalid geojson (invalid coordinates format, missing outer list)
INVALID_COORD_LIST = '{ "type": "Polygon", "coordinates": [ [ 1208064, 624154 ], [ 1208064, 601260 ], [ 1231345, 601260 ], [ 1231345, 624154 ], [ 1208064, 624154 ] ] }'

## invalid geojson (invalid coordinates for Polygon, only 2)
TWO_COORDS = '{ "type": "Polygon", "coordinates": [ [ [ 12, 62 ], [ 12, 60 ] ] ] }'

## invalid geojson (invalid coordinates, not a Polygon)
NON_POLY = '{ "type": "Polygon", "coordinates": [ [ [ 12, 62 ], [ 12, 60 ], [ 12, 62 ], [ 12, 60 ] ] ] }'

## invalid geojson-polygon (not a valid "type")
INVALID_TYPE = '{ "type": "Poli", "coordinates": [ [ [ 1208064, 624154 ], [ 1208064, 601260 ], [ 1231345, 601260 ], [ 1231345, 624154 ], [ 1208064, 624154 ] ] ] }'

## invalid geojson-polygon (not a type="Polygon")
TYPE_LINE_STR = '{ "type": "LineString", "coordinates": [ [ [ 1208064, 624154 ], [ 1208064, 601260 ], [ 1231345, 601260 ], [ 1231345, 624154 ], [ 1208064, 624154 ] ] ] }'

##------------------------------------------------------------------------
def test_exception_on_invalid_geojson():
    ## Test check_polygon_intersection() for raise(InvalidGeoJson) on invalid GeoJSON format
    with pytest.raises(InvalidGeoJson):
        result = check_polygon_intersection(NON_POLY, POLY_GOOD) 

##------------------------------------------------------------------------
## Test get_overlap_area() with multiple sets of inputs with BAD json or BAD geojson
## All should raise InvalidGeoJson()
@pytest.mark.parametrize("poly_bad, poly_good", [ 
   (POLY_GOOD, NULLSTR),
   (POLY_GOOD, QUOTES),
   (POLY_GOOD, ASTER),
   (POLY_GOOD, "bogus-str"),
   (POLY_GOOD, EMPTYLIST),
   (POLY_GOOD, EMPTYDICT),
   (POLY_GOOD, BAD_COORDINATES),
   (POLY_GOOD, BAD_TYPE),
   (POLY_GOOD, BAD_COORD_LIST),
   (POLY_GOOD, INVALID_COORD_LIST),
   (POLY_GOOD, TWO_COORDS),
   (POLY_GOOD, NON_POLY),
   (POLY_GOOD, INVALID_TYPE),
   (POLY_GOOD, TYPE_LINE_STR)
  ])
def test_exception_on_bad_geojson(poly_bad,poly_good):
    with pytest.raises(InvalidGeoJson):
        l_polys = [poly_bad, poly_good]
        result = get_overlap_area(*l_polys) 
