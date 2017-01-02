
from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from multiselectfield import MultiSelectField

import uuid

ACTIONS = (
            ('get', 'GET'),
            ('post', 'POSt'),
            ('put', 'PUT'),
            ('delete', 'DELETE'),
        )

class Resource(models.Model):
    """
    """
    name = models.CharField(_('Resource Name'),max_length=50)
    host = models.CharField(_('Request HOST'), max_length=50)
    request_path = models.CharField(_('request path of API'), max_length=50)
    resource_end_point = models.URLField(_('End Point used by Process'), max_length=255, editable=False, unique=True)
    actions = MultiSelectField(_('Resource allowed Methods'), default=1, choices=ACTIONS)
    headers = JSONField(_('Keys for request Headers'), help_text='sperated via comma , ', blank=True, null=True)
    body = JSONField(_('Keys for request Query params'), help_text='sperated via comma , ', blank=True, null=True)
    data = JSONField(_('Keys for request post data'), help_text='sperated via comma , ', blank=True, null=True)
    added_at = models.DateTimeField(_('added at'), auto_now_add=True)

    class Meta:
        unique_together = ('host', 'request_path',)

    def __str__(self):
        return '{name}'.format(
            name=self.name,
            )

    def clean(self):
        """
        """
        if not self.request_path.endswith('/'):
            self.request_path = '{0}/'.format(self.request_path)

        if not self.host.endswith('/') and not self.request_path.startswith('/'):
            self.host = '{0}/'.format(self.host)

    def save(self, *args, **kwargs):
        """
        """
        self.resource_end_point = 'http://{0}.veris.in/{1}'.format(str(uuid.uuid4()), self.request_path)
        return super(Resource, self).save(*args, **kwargs)

class ResourceAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('name', 'resource_end_point', 'allowed_methods', )
    list_display_links = ('name', 'resource_end_point',)
    exclude=('resource_end_point', )

    def allowed_methods(self, obj):
        """
        """
        if obj.actions:
            return str(obj.actions)
        return None

admin.site.register(Resource, ResourceAdmin)
