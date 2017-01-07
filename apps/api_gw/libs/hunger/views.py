
from django.conf import settings
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes


class HelloView(View):
    """
    """

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(HelloView, self).dispatch(*args, **kwargs)

    def post(self, request):
        # <view logic>
        return JsonResponse({'response':'Hellooooo'})


class Hello_X_View(View):
    """
    """

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Hello_X_View, self).dispatch(*args, **kwargs)

    def post(self, request):
        if not request.POST.get('name'):
            return JsonResponse({'detail':'name key not present in POST body'}, status=400)
        # <view logic>
        response = 'Hello {0}'.format(request.POST.get('name'))
        return JsonResponse({'response':response}, status=200)