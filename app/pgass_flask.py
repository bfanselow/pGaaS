#!/usr/bin/python3

"""

  Module: pgaas_flask.py
  Description: Provides main() for pGaaS Flask application
  Author: William Fanselow
  Last update: 2020-03-10 

  NOTES:
   *  Test routes: $ export FLASK_APP='pgaas_flask'; flask routes

"""
## Standard python libs
import sys
import os
import traceback

## The "request" context contains request-specific variables containing the information needed to process the request
from flask import request, render_template, jsonify
from werkzeug.exceptions import * 
from jinja2.exceptions import * 

BASE_DIR = os.environ.get('BASE_DIR', None) ## set in *.wsgi
if not BASE_DIR:
  BASE_DIR = os.path.dirname(os.path.realpath(__file__))

## Custom flask modules 
import app_factory
from api_authorization import ApiAuthorizationError
##---------------------------------------------------------------------------------------
## Local configuration settings. This is separate from app.config settings, for flexibility
DEBUG = 0 

##---------------------------------------------------------------------------------------
## Create the Flask app instance from the app_factory
d_init = {'DEBUG': DEBUG}
app = app_factory.create_app(d_init)

##---------------------------------------------------------------------------------------
def error_response(e):
  gmtime_now = utils.gmt_now()
  etype = e.__class__.__name__ 
  code = getattr(e, 'code', 500) 
  d_response = {'timestamp': gmtime_now, 'exception': etype, 'message':str(e)}
  return(d_response)

##---------------------------------------------------------------------------------------

##---------------------------------------------------------------------------------------
##
## Register some initialization tasks to be done before every request is processed.
## NOT USED
@app.before_request  
def request_init():
  ###print(">>BEFORE-REQUEST (%s)" % (request.path))
  pass

##---------------------------------------------------------------------------------------
##
## Register some error handlers
##
@app.errorhandler(404)
def not_found_error(error):
  msg = "Requested URL (%s) not supported" % (request.url)
  app.logger.error("SARS unsupported URL (%s)" % (request.url))
  d_response = { "message": msg } 
  return jsonify(error=d_response)

@app.errorhandler(HTTPException)
def http_error(e):
  d_response = error_response(e)
  if '/api/' in request.path:
    return jsonify(error=d_response)
  else:
    return render_template('error.html', **d_response)

@app.errorhandler(TemplateNotFound)
def template_not_found(e):
  d_response = error_response(e)
  return render_template('error.html', **d_response)

@app.errorhandler(ApiAuthorizationError)
def api_error(e):
  d_response = error_response(e)
  return jsonify(error=d_response)

@app.errorhandler(Exception)
def exception_error(e):
  d_response = error_response(e)
  tb_str = ''.join(traceback.format_tb(e.__traceback__))
  app.logger.error("Exception traceback: %s" % (tb_str))
  return jsonify(error=d_response)

##---------------------------------------------------------------------------------------
##
## Register some "cleanup" tasks after every request is processed.
## Functions decorated with "teardown_request" behave similarly to "after_request"
## functions, however, they have the added benefit of being triggered regardless of 
## any exceptions raised. 
##
#@app.teardown_appcontext
#def teardown(msg):

##---------------------------------------------------------------------------------------
## Handle favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

##############################################################################
##
## For testing from command-line (rather than via WSGI)
## Starts an internal (low-load) web-server
##
##############################################################################
if __name__ == '__main__':
  print("Testing Flask app from CLI...")
  #print("PYTHON-PATH=%s" % (sys.path))

  #app.run(host="10.40.161.251", port=8080)
  app.run(port=8080)
  print("\nExiting. See you next time!\n")
