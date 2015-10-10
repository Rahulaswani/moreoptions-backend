from django.shortcuts import render
from django.http import Http404

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
    return Response(get_result(request.body))
