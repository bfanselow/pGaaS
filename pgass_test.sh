#!/bin/sh

## Simple tests of Flask service.
## This is not a thorough testing of GeoJSON validation. See tests/ dir for that. 

curl="/usr/bin/curl"

## GET (i.e. no  payload)
echo "Testing GET request..."
$curl http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## GET (unsupported endpoint)
echo "Testing GET request to unsupported endpoint..."
$curl http://127.0.0.1:8080/api/bogus_endpoint
echo ""
echo ""
sleep 2

## POST (Empty payload)
echo "Testing POST (emtpy payload)..."
$curl -H '{"Content-Type":"application/json"}' -d '{}' http://127.0.0.1:8080/api/polygon_intersection
echo ""
echo ""
sleep 2

## POST (No API key)
echo "Testing POST (no api key)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"hello":"bill"}' http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## POST (Invalid API key)
echo "Testing POST (invliad api key)..."
curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"pgass-test"}' http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## POST (No "polygons" key)
echo "Testing POST (no polygons list)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test"}' http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## POST (Only one polygon in "polygons" list)
echo "Testing POST (single polygon)..."
curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [ { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## POST (Invalid "polygons")
echo "Testing POST (invalid polygons)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": ["foo", "bar"]}' http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## POST (successful identification of intersection)
echo "Testing POST (intersecting polygons)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
echo ""
echo ""
sleep 2

## POST (successful identification of overlap)
echo "Testing POST (polygon overlap)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## POST (successful identification of NON-intersection)
echo "Testing POST (non-intersecting polygons)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
echo ""
echo ""
sleep 2

## POST (successful identification of NON-overlap)
echo "Testing POST (polygon non-overlap)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap_area
echo ""
echo ""
sleep 2

## POST (successful identification of point-in-polygon)
echo "Testing POST (point-in-polygon)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygon": { "type": "Polygon", "coordinates": [[[24.950899, 60.169158], [24.953492, 60.169158], [24.953510, 60.170104], [24.950958, 60.169990], [24.950899, 60.169158]]] }, "point": { "type": "Point", "coordinates": [24.952242, 60.1696017] } }' http://127.0.0.1:8080/api/point_in_polygon
echo ""
echo ""
sleep 2

## POST (successful identification of point-NOT-in-polygon)
echo "Testing POST (point-NOT-in-polygon)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygon": { "type": "Polygon", "coordinates": [[[24.950899, 60.169158], [24.953492, 60.169158], [24.953510, 60.170104], [24.950958, 60.169990], [24.950899, 60.169158]]] }, "point": { "type": "Point", "coordinates": [240.42, 10.17] } }' http://127.0.0.1:8080/api/point_in_polygon

