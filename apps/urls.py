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
        url(r'^widg/', include('apps.api_gw.widgets.routers')),   
]


