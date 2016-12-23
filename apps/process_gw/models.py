
from django.contrib import admin
from django.contrib.admin.decorators import register
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


class Runtime(models.Model):
    runtime_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    runtime_type = models.CharField(unique=True, max_length=64, null=False, blank=False)

    def __str__(self):
        return self.runtime_type


class RequestSession(models.Model):
    """
    """
    runtime = models.ForeignKey(Runtime)
    requestId = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    request_type = models.CharField(_('Request type'), max_length=20, choices=REQUEST_TYPES)
    state = models.CharField(_('current state of a request'), max_length=20, choices=REQUEST_STATES)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True, db_index=True)

    def __str__(self):
        return '{requestId}'.format(
            requestId=str(self.requestId)
            )

class RequestTrace(models.Model):
    """
    """
    request = models.ForeignKey(RequestSession, related_name='request_session', verbose_name='individual request session id')
    parent_request = models.ForeignKey(RequestSession, related_name='vrt_session', verbose_name='entire runtime session')
    state = models.CharField(_('state of a request'), max_length=20, choices=REQUEST_STATES)
    payload = JSONField(_('Request payload'), blank=True, null=True)
    response = JSONField(_('Request Response'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)

    def __str__(self):
        return '{requestId}'.format(
            requestId=str(self.request.requestId)
            )


@register(Runtime)
class RuntimeAdmin(admin.ModelAdmin):
    list_display = ('runtime_id', 'runtime_type')


class RequestSessionAdmin(admin.ModelAdmin):
    list_display = ('requestId', 'request_type', 'state', 'runtime')
    list_display_links = ('requestId', )

class RequestTraceAdmin(admin.ModelAdmin):
    list_display = ('request', 'parent_request', 'request_type', 'state', )
    list_display_links = ('request', )

    def request_type(self, obj):
        return obj.request.request_type

admin.site.register(RequestSession, RequestSessionAdmin)
admin.site.register(RequestTrace, RequestTraceAdmin)