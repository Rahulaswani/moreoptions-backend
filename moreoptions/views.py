from django.shortcuts import render
from django.http import Http404
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from server.server import *

import json

class MoreOptions(APIView):
  """
    Get more options for product.
  """
  def put(self, request, format=None):
    keyword = json.loads(request.body)['productName']
    if cache.get(keyword) != None:
      return Response(cache.get(keyword))
    result = get_result(request.body)
    # timeout of 15 minutes.
    cache.set(keyword, result)
    return Response(result)
