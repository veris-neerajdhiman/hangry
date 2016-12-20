
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

class RequestSession(models.Model):
    """
    """
    reuestId = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    state = models.CharField(_('current state of a process'), max_length=20, choices=REQUEST_STATES)

    def __str__(self):
        return self.reuestId

class RequestTrace(models.Model):
    """
    """
    request = models.ForeignKey(RequestSession)
    state = models.CharField(_('state of a process'), max_length=20, choices=REQUEST_STATES)
    payload = JSONField(_('widgets config, for internal use'))
    response = JSONField(_('widgets config, for internal use'))

    def __str__(self):
        return self.request

class RequestSessionAdmin(admin.ModelAdmin):
    list_display = ('reuestId', 'state', )
    list_display_links = ('reuestId', )

class RequestTraceAdmin(admin.ModelAdmin):
    list_display = ('request', 'state', )
    list_display_links = ('request', )

admin.site.register(RequestSession, RequestSessionAdmin)
admin.site.register(RequestTrace, RequestTraceAdmin)