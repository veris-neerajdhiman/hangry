from rest_framework import serializers
from apps.api_gw.terminals.models import Terminals

from apps.api_gw.widgets.serializers import WidgetSerializer


class TerminalSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True)

    class Meta:
        model = Terminals
        fields = '__all__'