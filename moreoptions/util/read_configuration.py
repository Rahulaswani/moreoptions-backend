#!/usr/bin/python
#
# Copyright (c) 2015 MoreOptions. All rights reserved.
#
# Author: ankush@moreoption.co
#
# This class implements the helper functions for readin json configuration files.
#

import os
import json
import sys

class ReadConfiguration(object):
  def __init__(self):
    pass

  def read_conf(self, file_name):
    with open(file_name) as data_file:    
      data = json.load(data_file)
    return data
