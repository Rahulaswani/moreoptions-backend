#!/usr/bin/python
#
# Copyright (c) 2015 MoreOptions. All rights reserved.
#
# Author: ankush@moreoption.co
#
# This class implements the helper functions for flipkart api
#

import os
import pycurl
import string

from StringIO import StringIO

class Request(object):
  def __init__(self):
    pass

  def send_request(self, url, headers):
    buff = StringIO()
    get_conn = pycurl.Curl()
    get_conn.setopt(get_conn.URL, url.replace(" ", "%20"))
    get_conn.setopt(get_conn.FOLLOWLOCATION, 1)
    get_conn.setopt(get_conn.HTTPHEADER, headers)
    get_conn.setopt(get_conn.WRITEFUNCTION, buff.write)
    get_conn.perform()
    get_conn.close()
    return buff.getvalue()
