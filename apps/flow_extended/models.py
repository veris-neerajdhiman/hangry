"""
"""

from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

import uuid


APPS = ('vrt', 'widget', 'process', 'resource',)

RUNTIME = ('user', 'terminal')

VRT_APPS = (
        (APPS[0], 'Veris Run-Time'),
        (APPS[1], 'Widget'),
        (APPS[2], 'Process'),
        (APPS[3], 'Rsource'),    )

VRT_TYPES = (
        (RUNTIME[0], 'User Veris RunTime'),
        (RUNTIME[1], 'Terminal Veris RunTime'),
    )

class BaseModel(models.Model):
    """
    """
    requestId = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    start_at = models.DateTimeField(_('started at'), db_index=True)
    ends_at = models.DateTimeField(_('ended at'), db_index=True, null=True, blank=True)

    class Meta:
        abstract = True


class VRT(BaseModel):
    """
    """
    # widgets_enabled = JSONField(_('enabled widget for VRT'), blank=True, null=True)
    vrt_type = models.CharField(_('Type of VRT'), max_length=10, choices=VRT_TYPES)
    app_type = models.CharField(_('Type of Apps'), max_length=10, choices=VRT_APPS)



class VRTAdmin(admin.ModelAdmin):
    list_display = ('id', 'requestId', 'app_type', 'start_at', 'ends_at')
    list_display_links = ('requestId', 'id')


admin.site.register(VRT, VRTAdmin)