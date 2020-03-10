"""
 Module: config.py
 Description:
   BaseConfig() class (and child classes) for Flask application configuration for
   multiple environments.  Default configs are set in BaseConfig() attributes. Child
   classes of BaseConfig() used for each specific environment. 

"""
import os

##====================================================================================
class BaseConfig(object):
  """
  Base (Default) Application Configuration settings
  """ 

  DEBUG = False 
  TESTING = True
  VERSION = 1.0

  APP_CONTACT = 'bfanselow@gmail.com'

  ##==================================
  ## App paths
  ##==================================
  ## Directory containing this file
  ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

  ## Logfile directory and path (NOT USED)
  ##LOG_DIR = os.path.join(ROOT_DIR, 'log') 
  ##LOGFILE_PATH = LOG_DIR + '/pgaas.log'

  ##==================================
  ## Anonymous user stuff 
  ##==================================
  API_KEY = 'fanselow-pgass-test'

##====================================================================================
##====================================================================================
class ProductionConfig(BaseConfig):
  """
  Production Environment Configurations
  """ 
  DEBUG = False
  TESTING = False

##====================================================================================
class DevelopmentConfig(BaseConfig):
  """
  Development Environment Configurations
  """ 
  DEBUG = False 
  TESTING = False

##====================================================================================
class TestingConfig(BaseConfig):
  """
  Testing Environment Configurations
  """ 
  DEBUG = False 
  TESTING = True

