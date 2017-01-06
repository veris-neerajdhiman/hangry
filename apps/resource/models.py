
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
        we need to make host and request path clean so that both can have uniform structire in db
        it will redcude our pain while validation and concatenation
        """
        # clean request path
        # - if request path startwith '/' then remove it 
        # - if request path not ends with '/' then append '/' in the end
        if not self.request_path.endswith('/'):
            self.request_path = '{0}/'.format(self.request_path)

        # clean host
        #  - if host not ends with '/' the append '/' (remember request do not start with '/')
        if not self.host.endswith('/'):
            self.host = '{0}/'.format(self.host)

    def save(self, *args, **kwargs):
        """
        """
        sub_domain = str(uuid.uuid4())
        if self.id:
            temp = self.resource_end_point.split('://')
            temp = temp[1].split('.veris')
            sub_domain = temp[0]

        self.resource_end_point = 'http://{0}.veris.in/{1}'.format(sub_domain, self.request_path)
        return super(Resource, self).save(*args, **kwargs)


# ******************** Resource extended Verison ***************************



class ResourceExtended(models.Model):
    """
    """
    name = models.CharField(_('Resource Name'),max_length=50)
    upstream_url = models.CharField(_('Request HOST'), max_length=50)
    request_path = models.CharField(_('request path of API'), max_length=50)
    methods = MultiSelectField(_('Resource allowed Methods'), default=1, choices=ACTIONS)
    headers = JSONField(_('Define your headers here'), help_text='follow some standard rule, explained in respective models file', blank=True, null=True)
    body = JSONField(_('Define your Query params here'), help_text='follow some standard rule, explained in respective models file', blank=True, null=True)
    data = JSONField(_('Define your Post data here'), help_text='follow some standard rule, explained in respective models file', blank=True, null=True)
    added_at = models.DateTimeField(_('added at'), auto_now_add=True)

    class Meta:
        unique_together = ('upstream_url', 'request_path',)

    def __str__(self):
        return '{name}'.format(
            name=self.name,
            )



# Format for Headers : 
'''
{
    "Key": "Authorization",
    "sample": "token **************",
}
'''


# Format for body & data : 
'''
{
    "name": "name",
    "description": "field description",
    "label": "Name",
    "type": "string",
    "required": true,
    "validation": {"not_empty": {"on_fail": "Display name must not be empty."}}
    "values": [] # in case of list field
}
'''

# field types 
'''
    string: defines a string field (i.e. varchar or char , len - 255).Optional properties are allow_null, default, values, and validation.

    text: defines a large string field.Optional properties are allow_null, default and validation.

    binary: defines a binary string field.Optional properties are allow_null, default and validation.

    boolean: defines a boolean field.Optional properties are allow_null, default and validation.

    integer: defines an integer field.Optional properties are allow_null, default, values, and validation.

    float: defines a standard single-precision float field.Optional properties are allow_null, default and validation.

    datetime: a datetime field. Optional properties are allow_null, default, values, and validation.

    date: a date field. Optional properties are allow_null, default, values, and validation.

    time: a time field. Optional properties are allow_null, default, values, and validation.

    timestamp: a date and time stamp with timezone awareness where applicable.
'''

# Validations : 

# format
'''
{
    "validation":
    {
      "<validation_name>":
        {
          "on_fail" : "[ignore_field | <error_msg>]"
          <other_config>,
          ...
        },
      ...
    }
}

where on_fail is a configuration option that takes either the value ignore_field,
dictating if the field should be ignored if it does not pass validation,
or a specified error message to overwrite the generic exception thrown.
If this configuration is missing, a generic exception will be thrown stating the validation has failed. 
'''

# types
'''
picklist - Supported for string type only. It requires the field value to be set to one of the values listed in the values property. 

multi_picklist - similar to picklist but allows multiple values to be selected and stored.

read_only - sets this field as read only. Use "default” property to set values.

not_null - validates that the field value to be set is not null. Supported for all types,

not_empty - validates that the field value to be set is not empty string. Supported for string and text types. Null is not checked.

not_zero - validates that the field value to be set is not zero (0). Supported for integers, floats. Null is not checked.

int - validates that the value to be set isinteger values designated. Supported for integers.

float - validates that the value to be set is a valid float.

boolean - validates that the value to be set is one of the generally accepted values for true or false, i.e. true = 1, "1", "true", "on" and "yes". false = 0, "0", "false", "off", "no", and "".

email - validates that this field is an email, i.e. "name@company.com”. Supported for string type only.

url - validates that this field is a url, i.e. starts with "http(s)://”. Supported for string type only.

'''


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


class ResourceExtendedAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('name', 'upstream_url', 'request_path', 'allowed_methods', )
    list_display_links = ('name', 'upstream_url',)

    def allowed_methods(self, obj):
        """
        """
        if obj.methods:
            return str(obj.methods)
        return None

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceExtended, ResourceExtendedAdmin)







