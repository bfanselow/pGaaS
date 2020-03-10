"""
 File: utils.py
 Description: Common util functions for Flask app

"""
import datetime

##----------------------------------------------------------------------------------------------
def gmt_now(format=None):
  """ 
    Get the current timestamp string in UTC.
    Args:
     * Optional datetime formatting.
    Return: (datetime-str) String representation of the timestamp in UTC timezone.
  """ 

  default_format = "%Y-%m-%d %H:%M:%S"
  if format is None:
    format = default_format

  o_dt = datetime.datetime.now()
  gmtime_now = o_dt.strftime(format) 

  return(gmtime_now)

##----------------------------------------------------------------------------------------------
