#!/bin/sh

curl="/usr/bin/curl"

## GET (i.e. no  payload)
echo "Testing GET request..."
$curl http://127.0.0.1:8080/api/polygon_union
echo ""
echo ""

## POST (Empty payload)
echo "Testing POST (emtpy payload)..."
$curl -H '{"Content-Type":"application/json"}' -d '{}' http://127.0.0.1:8080/api/polygon_intersection
echo ""
echo ""

## POST (No API key)
echo "Testing POST (no api key)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"hello":"bill"}' http://127.0.0.1:8080/api/polygon_union
echo ""
echo ""

## POST (No "polygons" key)
echo "Testing POST (no polygons list)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test"}' http://127.0.0.1:8080/api/polygon_union
echo ""
echo ""

## POST (Invalid "polygons")
echo "Testing POST (invalid polygons)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": ["foo", "bar"]}' http://127.0.0.1:8080/api/polygon_union
echo ""
echo ""

## POST (successful identification of intersection)
echo "Testing POST (intersecting polygons)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
echo ""
echo ""

## POST (successful identification of UNION)
echo "Testing POST (polygon union)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_union
echo ""
echo ""

## POST (successful identification of NON-intersection)
echo "Testing POST (non-intersecting polygons)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
echo ""
echo ""

## POST (successful identification of NON-UNION)
echo "Testing POST (polygon non-union)..."
$curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_union
