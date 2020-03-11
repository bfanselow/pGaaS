#!/bin/sh

## Simple tests of Flask service.
## This is not a thorough testing of GeoJSON validation. See tests/ dir for that. 

curl="/usr/bin/curl"

## GET (i.e. no  payload)
echo "Testing GET request..."
$curl http://127.0.0.1:8080/api/polygon_overlap
echo ""
echo ""
sleep 2

## GET (unsupported endpoint)
echo "Testing GET request to unsupported endpoint..."
$curl http://127.0.0.1:8080/api/bogus_endpoing
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
$curl -H '{"Content-Type":"application/json"}' -d '{"hello":"bill"}' http://127.0.0.1:8080/api/polygon_overlap
echo ""
echo ""
sleep 2

## POST (No "polygons" key)
echo "Testing POST (no polygons list)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test"}' http://127.0.0.1:8080/api/polygon_overlap
echo ""
echo ""
sleep 2

## POST (Invalid "polygons")
echo "Testing POST (invalid polygons)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": ["foo", "bar"]}' http://127.0.0.1:8080/api/polygon_overlap
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
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap
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
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap
