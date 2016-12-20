from rest_framework import serializers
from apps.api_gw.widgets.models import Widgets


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widgets
        fields = '__all__'