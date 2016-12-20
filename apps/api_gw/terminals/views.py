
from django.conf import settings
from django.views import View
from django.http import HttpResponse


from rest_framework import viewsets, status
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes


class HelloView(View):
    """
    """
    def get(self, request):
        # <view logic>
        return HttpResponse('Hellooooo')


class Hello_X_View(View):
    """
    """
    def get(self, request):
        # <view logic>
        return HttpResponse('Hellooooo--X')