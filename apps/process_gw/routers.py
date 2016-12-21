#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include
from django.conf import settings
from apps.process_gw import views


vrt_resolve = views.RuntimeViewSet.as_view({
    'get': 'vrt_resolve',
})

widget_resolve = views.RuntimeViewSet.as_view({
    'get': 'widget_resolve',
    'post': 'widget_resolve',
})

process_resolve = views.RuntimeViewSet.as_view({
    'get': 'process_resolve',
    'post': 'process_resolve',
})




urlpatterns = [
        url(r'^vrt/(?P<vrt_id>[0-9]+)/$', 
            vrt_resolve, 
            name='vrt-resolve'),   
        url(r'^vrt/(?P<vrt_id>[0-9]+)/widget/(?P<widget_id>[0-9]+)/$', 
            widget_resolve, 
            name='widget-resolve'),   
        url(r'^vrt/(?P<vrt_id>[0-9]+)/widget/(?P<widget_id>[0-9]+)/process/(?P<process_id>\w+)/$', 
                process_resolve, 
                name='process-resolve'),   
]
