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

urlpatterns = [
        url(r'^vrt/(?P<vrt_id>[0-9]+)/', views.RuntimeViewSet.as_view(), name='vrt'),   
]


