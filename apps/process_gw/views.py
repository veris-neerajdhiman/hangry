
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from rest_framework.views import APIView

# from apps.api_gw.widgets.models import Widgets
# from apps.api_gw.widgets import serializers


class RuntimeViewSet(APIView):
    """
    """
    def get(self, request, vrt_id, format=None):
        """
        """
        return Response({'vrt_id':vrt_id})

