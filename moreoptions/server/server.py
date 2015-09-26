#!/usr/bin/env python
import json
import pycurl
import random
import string
import sys
import urllib
import urllib2
import web
import xml.etree.ElementTree as ET

from apps.flipkart import *
from StringIO import StringIO
from urllib import urlencode
from util.read_configuration import *


def get_result(data):
  #TODO: Go over all the apps to call and call send_request for those
  file_name = "/root/workshop/moreoptions-backend/moreoptions/config/apps.json"
  read_configuration = ReadConfiguration()
  apps = read_configuration.read_conf(file_name)
  for key, value in apps.iteritems():
    api = globals()[value]()
    return api.get_more_options(data)  

urls = (
    '/put', 'moreoptions_put',
)

class moreoptions_put:
 def PUT(self):
   try:
     data = web.data() 
     #TODO: If name is null then do something.
     return get_result(data)
   except Exception, e:
     print str(e)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
