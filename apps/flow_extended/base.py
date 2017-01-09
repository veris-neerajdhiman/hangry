"""
"""

from datetime import datetime

import uuid

from rest_framework import viewsets, status

from apps.flow_extended.models import VRT, RUNTIME

class BaseApp(viewsets.GenericViewSet):
    """ base implementation of all apss, below is an minimum example
    to extend this class

    .. code-block:: python

        class MyApp(BaseApp):

            # declare supported schemes here
            __app__ = 'vrt'

          
    """

    # supported apps, ex. ['vrt', 'widget', 'process', 'resource']
    __app__ = None

    # supported runtime, ex. ['user', 'terminal']
    __runtime__ = None

    model = VRT

    def __init__(self):
        """ 
        initial variables
        """
        self.__obj = None
        self.vrt_type = None
        self.start_time = datetime.now()

    def initialize(self, *args, **kwargs):
        """
        service will initaized from here
        """
        if self.__runtime__ not in RUNTIME:
            raise EnvironmentError('UnKnown Runtime Environment.')

        # if self.__app__ is 'vrt':
        #     self.__obj = self.model.objects.create(start_at=self.start_time, vrt_type=self.__runtime__)
        self.__obj = self.model.objects.create(start_at=self.start_time, vrt_type=self.__runtime__, app_type=self.__app__)

    def get_object(self):
        """
        return model object
        """
        return self.__obj

    def resolve(self, request, *args, **kwargs):
        """
        """
        self.initialize(*args, **kwargs)

        pass

    def validate(self):
        pass

    def ext_request(self, url, method):
        """ 
        request other service/app
        """
        pass

    def response(self):
        """
        """
        self.__obj.ends_at = datetime.now()
        self.__obj.save()
        pass