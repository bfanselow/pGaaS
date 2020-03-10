"""
 File: utils.py
 Description: Common util functions for Flask app

"""

##----------------------------------------------------------------------------------------------
def dprint(level, msg):
  """ Print debug messages """
  if level <= DEBUG:
    print("DEBUG (%d): %s" % (level, msg))
