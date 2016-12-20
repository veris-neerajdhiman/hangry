#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include
from django.conf import settings
from apps.api_gw.widgets import views

urlpatterns = [
        url(r'^hello/', views.HelloView.as_view(), name='hello-word'),   
        url(r'^hello-x/', views.Hello_X_View.as_view(), name='hello-X-word'),   

]


