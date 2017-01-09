#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include
from django.conf import settings
from apps.flow_extended import vrt, widgets, process


vrt_resolve = vrt.RuntimeViewSet.as_view({
    'get' : 'get',
    'post': 'resolve',
})

widget_resolve = widgets.WidgetViewSet.as_view({
    'post': 'resolve',
})

process_resolve = process.ProcessViewSet.as_view({
    'post': 'resolve',
})


urlpatterns = [
        url(r'^vrt/(?P<vrt_id>\w+)/$', 
            vrt_resolve, 
            name='vrt-resolve'),   

        url(r'^vrt/(?P<vrt_id>\w+)/widget/$', 
            vrt_resolve, 
            name='vrt-resolve'),   

        url(r'^vrt/(?P<vrt_id>\w+)/widget/(?P<widget_id>[0-9]+)/$', 
            widget_resolve, 
            name='widget-resolve'),

        url(r'^vrt/(?P<vrt_id>\w+)/widget/(?P<widget_id>[0-9]+)/process/(?P<process_id>\w+)/$', 
            process_resolve, 
            name='process-resolve'),

]
