#!/usr/bin/python
#
# Copyright (c) 2015 MoreOptions. All rights reserved.
#
# Author: ankush@moreoption.co
#
# This class implements the helper functions for flipkart api
#

import os
import json
import sys

from util.read_configuration import *
from util.net.request import *

class FlipkartApi(object):
  def __init__(self):
    self.request_ob = Request() 

  def get_more_options(self, data):
    """
    Function to get more options corresponding to data given for flipkart
    """
    name = self.get_product_name(data)
    if name == "":
      return {}
    result = self.send_request(name)
    return self.process_result(result)

  def get_product_name(self, data):
    """
    Given data find out the product name. As of now we are depending on ids.
    """
    js = json.loads(data)
    app_name = js['appName']
    name = js['productName']
    return name

  def send_request(self, product_name):
    """
    Function to send request to flipkart server.
    """
    file_name = "/root/workshop/moreoptions-backend/moreoptions/config/flipkart_api.json"
    read_configuration = ReadConfiguration()
    data = read_configuration.read_conf(file_name)
    url = data["url"] % (product_name)
    header = []
    header_json = data["headers"]
    for key in header_json:
      val = header_json[key]
      header.append(key + ": " + val)
    return self.request_ob.send_request(url, header) 

  def process_result(self, result):
    """
    Function to massage result according to our need.
    """
    json_output = json.loads(result)['productInfoList']
    json_result = []
    i = 0
    for prod in json_output:
      if i > 2:
        break
      i = i + 1
      attr = prod['productBaseInfo']['productAttributes']
      temp_ar = {}
      temp_ar['appName'] = "Flipkart"
      temp_ar['productName'] = attr['title']
      temp_ar['productImage'] = []
      for key, value in attr['imageUrls'].items():
        temp_pic = {}
        # get height width
        if key == "unknown":
          continue
        hw = key.split('x')
        temp_pic['width'] = hw[0]
        temp_pic['height'] = hw[1]
        temp_pic['url'] = value 
        temp_ar['productImage'].append(temp_pic)
      temp_ar['productSellingPrice'] = str(attr['sellingPrice']['amount'])
      temp_ar['productURL'] = attr['productUrl']
      json_result.append(temp_ar)
    return json.JSONEncoder().encode(json_result)
