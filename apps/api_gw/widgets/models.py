from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from apps.resource.models import Resource

class Widgets(models.Model):
    """
    """
    name = models.CharField(_('widget name'), max_length=100)
    config = JSONField(_('widgets config, for internal use'))
    resource = models.ForeignKey(Resource)

    def __str__(self):
        return self.name

class WidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('name', )


admin.site.register(Widgets, WidgetAdmin)