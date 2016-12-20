
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from apps.api_gw.widgets.models import Widgets
from apps.api_gw.widgets import serializers


class WidgetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Widgets.objects.all()
    serializer_class = serializers.WidgetSerializer
