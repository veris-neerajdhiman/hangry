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


class WidgetViewSet(BaseApp):
    """
    """
    __app__ = 'widget'
    serializer_class = utils.NoneSerializer
    __runtime__ = 'terminal'

    def __init__(self, *args, **kwargs):
        """
        """
        super(WidgetViewSet, self).__init__()
        self.__s = Session()

    def resolve(self, request, vrt_id, widget_id):
        """
        """
        super(WidgetViewSet, self).resolve(request)

        url = 'http://localhost:8000/vrt/{0}/widget/2/process/hello/'.format(self.__runtime__)

        resp = self.ext_request(url, 'POST')
        return Response(self.response(resp))

    def ext_request(self, url, method):
        """
        """
        return utils.service_rq(self.__s, method, headers={}, param={}, data={}, url=url)
        
    def response(self, resp):
        """
        """
        super(WidgetViewSet, self).response()
        return resp
