"""
  File: app_factory.py
  Description: Flask application "factory"
  Author: William Fanselow
  Last update: 2020-03-10 
"""
import sys
import os

from flask import Flask, request
from config import *

from blueprints.api.routes import bp_api
## FUTURE: from blueprints.ui.routes import bp_ui

DEBUG = 0

##---------------------------------------------------------------------------------------
def create_app(d_init):
  """
   Create Flask instance (app context).
   Return app object
  """
  
  app = Flask(__name__)

  ## ignore trailing slashes in a URL ("../myMethod/" is treated same as "/myMethod")
  app.url_map.strict_slashes = False

  ## load app configurations 
  _load_configs(app)

  ## set-up logging
  ##_setup_logging(app) 

  with app.app_context():

    _register_blueprints(app)

    if DEBUG > 1:
     _dump_info(app) ## prints to stderr (typically /var/log/httpd/error_log)
  
    return( app )

##---------------------------------------------------------------------------------------
def _load_configs(app):
  """Load app configuration settings"""
  print("Loading configs...")
  app.config.from_object(DevelopmentConfig)
  
  if DEBUG > 2:
    app.debug = True 

##---------------------------------------------------------------------------------------
def _register_blueprints(app):
  """Register all app blueprints"""

  ## Register routes from "api" blueprint object (bp_api)
  app.register_blueprint(bp_api)

  ## Register routes from "ui" blueprint object (bp_ui)
  ## FUTURE: app.register_blueprint(bp_ui)

##---------------------------------------------------------------------------------------
def _dump_info(app):
  """Output some app environment/config info for debug/troubleshooting"""
  print("PATH: %s" % (sys.path))

##---------------------------------------------------------------------------------------
