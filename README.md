# pGaaS

## Polygon-Geometry-as-a-Service

Simple service to perform polygon-geometry operations: intersection of 2 polygons, union of 2+ polygons

## Requirements:
 * geojson==2.5.0
 * Shapely==1.7.0
 * pytest==5.3.5


## Setup
```
 $ git clone https://github.com/bfanselow/pGaaS.git
 $ cd pGaaS/
 $ virtualenv -p python3 venv
 $ pip install -r requirements.txt
```

### Testing all test file in tests/ dir
```
## from pGaas dir
(venv) $ python -m pytest -v
```

### Run Flask dev server
