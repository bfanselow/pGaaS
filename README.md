# pGaaS

## Polygon-Geometry-as-a-Service

Simple service to perform polygon-geometry operations
 1) **intersection** of 2 polygons (in GeoJSON format): returns {"intersection":(0|1)}
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
{"intersection":1}
```
  
 2) **Union** of 2+ polygons: returns {"union":0} if no union, or {"union":{ __GeoJSON-PolygonObj__ }} if union
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_union
{"union":0}

$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_union
{"union":{"coordinates":[[[1219317.0,624154.0],[1231345.0,624154.0],[1231345.0,601260.0],[1208064.0,601260.0],[1208064.0,614453.0],[1199915.0,614453.0],[1199915.0,633079.0],[1219317.0,633079.0],[1219317.0,624154.0]]],"type":"Polygon"}}
```

## Requirements:
 * geojson==2.5.0
 * Shapely==1.7.0
 * pytest==5.3.5
 * Flask==1.1.1 (auto-installs lots of other pkgs)

## Notes:
* Engine for all GeoJSON work is **app/polygon_geometry.py** 
* You must include a "dummy" API key **{ "api_key":"fanselow-pgass-test"}** in all POST payloads, or in the HEADER {"X-Api-Key":"fanselow-pgass-test"}.  Obvioulsy, as is, this provides no real security, but serves a placeholder for future Security capability. 
* Shapley appears to not enforce the August 2016 (GeoJSON) IETF specification - validating objects from the old informal 2008 spec.  Some of the GeoJSON objects used in testing will pass validation but should techncially fail the "right-hand rule". 
* GeoJSON files for states (colorado, wyoming, montana) used for pytests sourced from https://eric.clst.org/tech/usgeojson/

## Setup
```
 $ git clone https://github.com/bfanselow/pGaaS.git
 $ cd pGaaS/
 $ virtualenv -p python3 venv
 $ pip install -r requirements.txt
```

### Testing all test-files in tests/ dir
```
## from pGaas dir
(venv) $ python -m pytest -v
```
### Run the Flask DEV server (NOT for production!!)
```
python app/pgass_flask.py
```

### Run with WSGI in Apache 
See pgass_flask.wsgi 

## Example REQUESTS/RESPONSES (failures and successes):
**GET (Empty payload)** 
```
$ curl http://127.0.0.1:8080/api/polygon_union
{"error":{"exception":"ApiAuthorizationError","message":"api_authorize: Request payload is not valid json","timestamp":"2020-03-10 19:31:38"}}
```

**POST (Empty payload)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{}' http://127.0.0.1:8080/api/polygon_intersection
{"error":{"exception":"ApiAuthorizationError","message":"API request authorization failed: no api-key in payload or headers","timestamp":"2020-03-10 21:11:22"}}
```

**POST (No API key)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"hello":"bill"}' http://127.0.0.1:8080/api/polygon_union
{"error":{"exception":"ApiAuthorizationError","message":"API request authorization failed: no api-key in payload or headers","timestamp":"2020-03-10 20:07:51"}}
```

**POST (No "polygons" key)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test"}' http://127.0.0.1:8080/api/polygon_union
{"error":{"exception":"ApiDataError","message":"Request payload must contain a list of 2 or more polygons","timestamp":"2020-03-10 20:28:31"}}
```

**POST (Invalid "polygons". See tests/ dir for more GeoJson validation tests)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": ["foo", "bar"]}' http://127.0.0.1:8080/api/polygon_union
{"error":{"exception":"InvalidGeoJson","message":"Invalid GeoJSON format: Expecting value: line 1 column 1 (char 0)","timestamp":"2020-03-10 20:39:28"}}
```

**POST (successful identification of intersection)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
{"intersection":1}
```

**POST (successful identification of UNION)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_union
{"union":{"coordinates":[[[1219317.0,624154.0],[1231345.0,624154.0],[1231345.0,601260.0],[1208064.0,601260.0],[1208064.0,614453.0],[1199915.0,614453.0],[1199915.0,633079.0],[1219317.0,633079.0],[1219317.0,624154.0]]],"type":"Polygon"}}
```

**POST (successful identification of NON-intersection)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
{"intersection":0}
```

**POST (successful identification of NON-UNION)** 
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_union
{"union":0}
```
