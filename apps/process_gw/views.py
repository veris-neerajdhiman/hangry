
from django.conf import settings

from rest_framework import viewsets, status, serializers
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from rest_framework.views import APIView

import requests


class NoneSerializer(serializers.Serializer):
    """
    """
    pass

class RuntimeViewSet(viewsets.GenericViewSet):
    """
    """
    serializer_class = NoneSerializer

    def vrt_resolve(self, request, vrt_id, format=None):
        """
        """
        url = '{0}/{1}/'.format('terminal', vrt_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.get(api, data=request.data, params=request.query_params, verify=True)
        return Response(response.json())

    def widget_resolve(self, request, vrt_id, widget_id, format=None):
        """
        """
        url = '{0}/{1}/{2}/{3}/'.format('terminal',vrt_id, 'widget', widget_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.get(api, data=request.data, params=request.query_params, verify=True)
        return Response(response.json())

    def process_resolve(self, request, vrt_id, widget_id, process_id, format=None):
        """
        """
        # import ipdb;ipdb.set_trace()
        url = '{0}/{1}/'.format('service', process_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.get(api, data=request.data, params=request.query_params, verify=True)
        return Response(response.json())

