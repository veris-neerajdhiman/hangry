
from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

# Create your models here.

import uuid


REQUEST_STATES = (
        ('init', 'Initialize'),
        ('inprocess', 'In Process'),
        ('wait', 'Waiting'),
        ('succeeded', 'Completed'),
        ('failed', 'Failed'),
    )

REQUEST_TYPES = (
        ('vrt', 'Veris RunTime'),
        ('widget', 'Widget'),
        ('process', 'Process'),
    )

class RequestSession(models.Model):
    """
    """
    requestId = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    request_type = models.CharField(_('Request type'), max_length=20, choices=REQUEST_TYPES)
    state = models.CharField(_('current state of a request'), max_length=20, choices=REQUEST_STATES)

    def __str__(self):
        return '{requestId}'.format(
            requestId=str(self.requestId)
            )

class RequestTrace(models.Model):
    """
    """
    request = models.ForeignKey(RequestSession)
    state = models.CharField(_('state of a request'), max_length=20, choices=REQUEST_STATES)
    payload = JSONField(_('widgets config, for internal use'), blank=True, null=True)
    response = JSONField(_('widgets config, for internal use'), blank=True, null=True)

    def __str__(self):
        return '{requestId}'.format(
            requestId=str(self.request.requestId)
            )


class RequestSessionAdmin(admin.ModelAdmin):
    list_display = ('requestId', 'request_type', 'state', )
    list_display_links = ('requestId', )

class RequestTraceAdmin(admin.ModelAdmin):
    list_display = ('request', 'request_type', 'state', )
    list_display_links = ('request', )

    def request_type(self, obj):
        return obj.request.request_type

admin.site.register(RequestSession, RequestSessionAdmin)
admin.site.register(RequestTrace, RequestTraceAdmin)