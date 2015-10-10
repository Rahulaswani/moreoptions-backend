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

from amazonproduct import API
from util.read_configuration import *
from util.net.request import *
from lxml import etree as ET

class AmazonApi(object):
  def __init__(self):
    pass

  def get_more_options(self, data):
    """
    Function to get more options corresponding to data given for flipkart
    """
    try:
      name = self.get_product_name(data)
      if name == "":
        return {}
      result = self.send_request(name)
      return self.process_result(result)
    except:
      return None 

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
    Function to send request to amazon server.
    """
    file_name = "/root/workshop/moreoptions-backend/moreoptions/config/amazon_api.json"
    read_configuration = ReadConfiguration()
    data = read_configuration.read_conf(file_name)
    #self.num_results = data["NumResults"]
    api = API(locale='us')
    items = api.item_search("All", Keywords = product_name, ResponseGroup='Large',ItemPage = 1)
    return items

  def process_result(self, result):
    """
    Function to massage result according to our need.
    """
    json_result = []
    i = 0
    for item in result:
      if i > 2:
        break
      i = i+1
      temp_ar = {}
      temp_ar['appName'] = "Amazon"
      temp_ar['productName'] = item.ItemAttributes.Title.text

      temp_pic = []
      temp_pic.append(item.SmallImage.URL.text)
      temp_pic.append(item.MediumImage.URL.text)
      temp_pic.append(item.LargeImage.URL.text)
      temp_ar['productImageUrls'] = temp_pic

      temp_ar['productSellingPrice'] = item.OfferSummary.LowestNewPrice.FormattedPrice.text
      temp_ar['productURL'] = item.DetailPageURL.text
      json_result.append(temp_ar)
    return json.JSONEncoder().encode(json_result)
