"""
Veris Runtime
"""
from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, status
from rest_framework.response import Response


from apps.flow_extended.base import BaseApp

from apps.api_gw.widgets.models import Widgets
from apps.flow_extended import utils

from requests import Session


class ProcessViewSet(BaseApp):
    """
    """
    __app__ = 'process'
    serializer_class = utils.NoneSerializer


    def __init__(self, *args, **kwargs):
        """
        """
        super(ProcessViewSet, self).__init__()
        self.__s = Session()
    
    def resolve(self, request, vrt_type, widget_id, process_id):
        """
        """
        self.__runtime__ = vrt_type
        super(ProcessViewSet, self).resolve(request)

        resp = self.ext_request()
        return Response(self.response(resp))

    def ext_request(self):
        """
        """
        url = 'http://localhost:8000/service/hello/'.format(self.__runtime__)
        return utils.service_rq(self.__s, 'POST', headers={}, param={}, data={}, url=url)
      

    def response(self, resp):
        """
        """
        super(ProcessViewSet, self).response()
        return resp