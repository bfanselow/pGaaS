# pGaaS

## Polygon-Geometry-as-a-Service

Simple service to perform polygon-geometry operations: intersection of 2 polygons, union of 2+ polygons

## Requirements:
 * geojson==2.5.0
 * Shapely==1.7.0
 * pytest==5.3.5
 * Flask==1.1.1 (auto-installs lots of other pkgs)

## Notes:
* Engine for all GeoJSON work is **app/polygon_geometry.py** 
* Shapley appears to not enforce the August 2016 (GeoJSON) IETF specification - validating objects from the old informal 2008 spec.  Some of the GeoJSON objects used in testing will pass validation but should techncially fail the "right-hand rule". 
* GeoJSON files for states (colorado, wyoming, montana) from https://eric.clst.org/tech/usgeojson/

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
