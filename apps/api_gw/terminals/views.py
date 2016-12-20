
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from apps.api_gw.terminals.models import Terminals
from apps.api_gw.terminals import serializers


class TerminalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = Terminals.objects.all()
    serializer_class = serializers.TerminalSerializer
