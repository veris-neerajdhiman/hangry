#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include
from django.conf import settings
from apps.api_gw.terminals import views

from rest_framework import routers

router = routers.SimpleRouter()


router.register(r'terminal', views.TerminalViewSet)

urlpatterns = [

]


urlpatterns += router.urls