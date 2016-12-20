from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _


from apps.api_gw.widgets.models import Widgets

# Create your models here.


class Terminals(models.Model):
    """
    """
    name = models.CharField(_('widget name'), max_length=100)
    widgets = models.ManyToManyField(Widgets)

    def __str__(self):
        return self.name

class TerminalsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('name', )


admin.site.register(Terminals, TerminalsAdmin)