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
import xmltodict

from amazonproduct import API
from util.aws_signed_request import *
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
      return json.JSONEncoder().encode([])

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
    public_key = 'AKIAIL2LL2XL7FQ5TIUQ'
    private_key = 'CPJixs1aPS1vPzw+eZpDUMeWl0BdMy+8mfTpJIBb'
    associate_tag = 'moreopti06-21'
    # generate signed URL
    request = aws_signed_request('in', {
      'Operation': 'ItemSearch',
      'Keywords': product_name,
      'SearchIndex': 'All',
      'ResponseGroup': 'Large',
      'ItemPage': '1',
       'sort' : 'relevancerank'}, public_key, private_key, associate_tag)

    # do request
    try:
      response_obj = urllib.urlopen(request);
    except IOError:
      print "Request failed."
      return ""
    else:
      response = response_obj.read()
      return response

  def process_result(self, result):
    """
    Function to massage result according to our need.
    """
    root = ET.fromstring(result)
    json_result = []
    j = 0
    i = 0
    for items in root:
      j = j + 1
      # first item is some operation info
      if j == 1:
        continue
      item_result = xmltodict.parse(ET.tostring(items))
      for item in item_result['Items']['Item']:
        if i > 2:
          return json.JSONEncoder().encode(json_result)
        i = i+1
        temp_ar = {}
        temp_ar['appName'] = "Amazon"
        temp_ar['productName'] = item['ItemAttributes']['Title']

        temp_pic = []
        temp_pic_small = {}
        temp_pic_small['url'] = item['SmallImage']['URL']
        temp_pic_small['height'] = str(item['SmallImage']['Height']['#text'])
        temp_pic_small['width'] = str(item['SmallImage']['Width']['#text'])

        temp_pic_medium = {}
        temp_pic_medium['url'] = item['MediumImage']['URL']
        temp_pic_medium['height'] = str(item['MediumImage']['Height']['#text'])
        temp_pic_medium['width'] = str(item['MediumImage']['Width']['#text'])

        temp_pic_large = {}
        temp_pic_large['url'] = item['LargeImage']['URL']
        temp_pic_large['height'] = str(item['LargeImage']['Height']['#text'])
        temp_pic_large['width'] = str(item['LargeImage']['Width']['#text'])

        temp_pic.append(temp_pic_small)
        temp_pic.append(temp_pic_medium)
        temp_pic.append(temp_pic_large)
        temp_ar['productImage'] = temp_pic

        temp_ar['productSellingPrice'] = item['OfferSummary']['LowestNewPrice']['FormattedPrice'].split(" ")[1]
        temp_ar['productURL'] = item['DetailPageURL']
        json_result.append(temp_ar)
    return json.JSONEncoder().encode(json_result)
