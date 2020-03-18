# pGaaS

## Polygon-Geometry-as-a-Service

### Simple (Python3/Flask) service to perform polygon-geometry operations
 1) **Intersection** of 2 polygons (in GeoJSON format).  
    - Endpoint: *api/polygon_intersection*   
    - POST Payload: 2 polygons in GeoJSON format  
    - Returns boolean identification of intersection:  {"intersects":(1|0)}
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
{"intersects":1}
```
  
 2) **Overlap Area** of 2 polygons.  
    - Endpoint:  *api/polygon_overlap_area*   
    - POST Payload: 2 polygons in GeoJSON format  
    - Returns overlap area (if any) of the two polygons: {"overlap_area": _float_}
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap_area
{"overlap_area":109165353.0}
```
 
 3) **Point-in-polygon** - is point within polygon boundry.  
    - Endpoint:  *api/point_in_polygon*   
    - POST Payload: 1 GeoJSON Polygon, 1 GeoJSON Point   
    - Returns boolean identification of whether or not polygon contains point:  {"is_within":(1|0)}
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygon": { "type": "Polygon", "coordinates": [[[24.950899, 60.169158], [24.953492, 60.169158], [24.953510, 60.170104], [24.950958, 60.169990], [24.950899, 60.169158]]] }, "point": { "type": "Point", "coordinates": [24.952242, 60.1696017] } }' http://127.0.0.1:8080/api/point_in_polygon
{"is_within":1}
```

## Requirements
 * geojson==2.5.0
 * Shapely==1.7.0
 * jsonschema==3.2.0 
 * pytest==5.3.5
 * Flask==1.1.1 (auto-installs lots of other pkgs)

## Notes
* Engine for all GeoJSON computations: **app/polygon_geometry.py** 
* You must include a "dummy" API key **{ "api_key":"fanselow-pgass-test"}** in all POST payloads, or in the HEADER {"X-Api-Key":"fanselow-pgass-test"}.  Obvioulsy, as is, this provides no real security, but serves a placeholder for future Security capability. 
* Shapley appears to not enforce the (2016) IETF GeoJSON specification - validating objects from the old informal 2008 spec.  Some of the GeoJSON objects used in testing will pass validation but should techncially fail the "right-hand rule", according to other public GeoJSON validators/linters.
* GeoJSON files for states (colorado, wyoming, montana) in data dir used for pytests sourced from https://eric.clst.org/tech/usgeojson/

## Setup
```
 $ git clone https://github.com/bfanselow/pGaaS.git
 $ cd pGaaS/
 $ virtualenv -p python3 venv
 $ source venv/bin/activate
 (venv) $ pip install -r requirements.txt
```

### Run the Flask DEV server for testing (NOT for production!!)
```
(venv) $ python app/pgass_flask.py

# For running in a production setting (with Apache) see pgass_flask.wsgi 
```

## Testing
### Test the GeoJSON computational methods with pytest
```
## from pGaaS dir (will run all test_* files in tests/ dir)
(venv) $ python -m pytest -v
```
### Test the Flask web-service 
```
## From pGaaS dir (with service running!)
## Using a seprate terminal or after backgrounding the service process (python app/pgass_flask.py > pg.log 2>&1 &)
(venv) $ ./pgass_test.sh
```

## Example REQUESTS/RESPONSES (failures and successes):
**GET *api/polygon_overlap_area*** (i.e. no  payload)
```
$ curl http://127.0.0.1:8080/api/polygon_overlap_area
{"error":{"exception":"ApiAuthorizationError","message":"api_authorize: Request payload is not valid json","timestamp":"2020-03-10 19:31:38"}}
```
**GET *api/bogus_endpoint*** (unsupported endpoint)
```
$ curl http://127.0.0.1:8080/api/bogus_endpoint
{"error":{"message":"Requested URL (http://127.0.0.1:8080/api/bogus_endpoint) not supported"}}
```

**POST *api/polygon_intersection*** (Empty payload)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{}' http://127.0.0.1:8080/api/polygon_intersection
{"error":{"exception":"ApiAuthorizationError","message":"API request authorization failed: no api-key in payload or headers","timestamp":"2020-03-10 21:11:22"}}
```

**POST  *api/polygon_overlap_area*** (No API key)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"hello":"bill"}' http://127.0.0.1:8080/api/polygon_overlap_area
{"error":{"exception":"ApiAuthorizationError","message":"API request authorization failed: no api-key in payload or headers","timestamp":"2020-03-10 20:07:51"}}
```

**POST *api/polygon_overlap_area*** (Invalid API key)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"pgass-test"}' http://127.0.0.1:8080/api/polygon_overlap_area
{"error":{"exception":"ApiAuthorizationError","message":"API request authorization failed - Invalid API-Key: (pgass-test)","timestamp":"2020-03-13 16:57:51"}}
```

**POST *api/polygon_overlap_area*** (No "polygons" key)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test"}' http://127.0.0.1:8080/api/polygon_overlap_area
{"error":{"exception":"ApiDataError","message":"Request payload must contain a list of 2 polygons","timestamp":"2020-03-10 20:28:31"}}
```

**POST *api/polygon_overlap_area*** (Only one polygon in "polygons" list)
```
curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [ { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap_area
{"error":{"exception":"ApiDataError","message":"Request payload must contain a list of 2 polygons","timestamp":"2020-03-11 17:24:46"}}
```

**POST *api/polygon_overlap_area*** (Invalid "polygons". See tests/ dir for more GeoJson validation tests)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": ["foo", "bar"]}' http://127.0.0.1:8080/api/polygon_overlap_area
{"error":{"exception":"InvalidGeoJson","message":"Invalid GeoJSON format: Expecting value: line 1 column 1 (char 0)","timestamp":"2020-03-10 20:39:28"}}
```

**POST *api/polygon_intersection*** (successful identification of intersection)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
{"intersects":1}
```
**POST *api/polygon_intersection*** (successful identification of NON-intersection)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_intersection
{"intersects":0}
```

**POST *api/polygon_overlap_area*** (successful identification of overlap)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[1199915, 633079], [1199915, 614453], [1219317, 614453], [1219317, 633079], [1199915, 633079]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap_area
{"overlap_area":109165353.0}
```

**POST *api/polygon_overlap_area*** (successful identification of NON-overlap)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygons": [{ "type": "Polygon", "coordinates": [[[1208064, 624154], [1208064, 601260], [1231345, 601260], [1231345, 624154], [1208064, 624154]]] }, { "type": "Polygon", "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]] } ]}' http://127.0.0.1:8080/api/polygon_overlap
{"overlap_area":0.0}
```

**POST *api/point_in_polygon*** (successful identification of point-in-polygon)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygon": { "type": "Polygon", "coordinates": [[[24.950899, 60.169158], [24.953492, 60.169158], [24.953510, 60.170104], [24.950958, 60.169990], [24.950899, 60.169158]]] }, "point": { "type": "Point", "coordinates": [24.952242, 60.1696017] } }' http://127.0.0.1:8080/api/point_in_polygon
{"is_within":1}
```

**POST *api/point_in_polygon*** (successful identification of point-NOT-in-polygon)
```
$ curl -H '{"Content-Type":"application/json"}' -d '{"api_key":"fanselow-pgass-test", "polygon": { "type": "Polygon", "coordinates": [[[24.950899, 60.169158], [24.953492, 60.169158], [24.953510, 60.170104], [24.950958, 60.169990], [24.950899, 60.169158]]] }, "point": { "type": "Point", "coordinates": [240.42, 10.17] } }' http://127.0.0.1:8080/api/point_in_polygon
{"is_within":0}
```
