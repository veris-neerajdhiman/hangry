#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include
from django.conf import settings


urlpatterns = [
        
        url(r'^service/', include('apps.api_gw.libs.urls')),   
        
        url(r'', include('apps.api_gw.terminals.routers')),   
        url(r'', include('apps.api_gw.widgets.routers')),   
        url(r'', include('apps.process_gw.routers')),   
        url(r'', include('apps.flow_extended.routers')),   
]


