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

from apps.amazon import *
from apps.flipkart import *

from multiprocessing import Process,Queue
from StringIO import StringIO
from urllib import urlencode
from util.read_configuration import *


def process_work(queue, data, value):
  api = globals()[value]()
  result = api.get_more_options(data)
  queue.put(result)

def get_result(data):
  #TODO: Go over all the apps to call and call send_request for those
  file_name = "/root/workshop/moreoptions-backend/moreoptions/config/apps.json"
  read_configuration = ReadConfiguration()
  apps = read_configuration.read_conf(file_name)
  processes = []
  queue = Queue()
  for key, value in apps.iteritems():
    p = Process(target=process_work, args = (queue, data, value))
    p.start()
    processes.append(p)

  for p in processes:
    p.join()

  result = []
  while not queue.empty():
    a = queue.get()
    for i in json.loads(a):
      result.append(i)
  return result
