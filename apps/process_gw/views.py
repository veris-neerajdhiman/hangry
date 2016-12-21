
from django.conf import settings

from rest_framework import viewsets, status, serializers
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView


from apps.process_gw.models import RequestSession, RequestTrace

import requests, uuid


class NoneSerializer(serializers.Serializer):
    """
    """
    pass

class RuntimeViewSet(viewsets.GenericViewSet):
    """
    """
    serializer_class = NoneSerializer

    def _merge_request_payload(self, request):
        """
        """
        payload = dict()

        payload.update({
            'get':request.query_params.dict(),
            'post':request.data.dict()
            })
        return payload

    def _create_request_session(self, type_,):
        """
        create initial session and trace for a request
        """
        session_id = uuid.uuid4().hex
        initial_session_data = {
            'state':'init',
            'requestId':session_id,
            'request_type':type_
            }

        return RequestSession.objects.create(**initial_session_data)

    def _update_request_session_state(self, session, state):
        """
        """
        return RequestSession.objects.filter(pk=session.pk).update(state=state)

    def _create_request_trace(self, session, state, payload, response=None):
        """
        """
        initial_trace_data ={
            'request':session,
            'state':state,
            'payload':payload,
            }

        if response:
            initial_trace_data.update({'response':response})

        return RequestTrace.objects.create(**initial_trace_data)

    def vrt_resolve(self, request, vrt_id, format=None):
        """
        """
        payload = self._merge_request_payload(request)

        # create session (state = init)
        session = self._create_request_session('vrt')        
        session_trace = self._create_request_trace(session, 'init', payload)

        # update session (state=in process)
        self._update_request_session_state(session, 'inprocess')
        session_trace = self._create_request_trace(session, 'inprocess', payload)

        # call API g/w
        url = '{0}/{1}/'.format('terminal', vrt_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.get(api, data=request.data, params=request.query_params, verify=True)

        request_response = self._manage_response(session, payload, response)      
        return Response(request_response)

    def widget_resolve(self, request, vrt_id, widget_id, format=None):
        """
        """
        payload = self._merge_request_payload(request)

        # valiadte payload
        session = self._validate_payload(request, 'widget', payload)

        # update session (state=in process)
        self._update_request_session_state(session, 'inprocess')
        session_trace = self._create_request_trace(session, 'inprocess', payload)

        # call API g/w
        url = '{0}/{1}/{2}/{3}/'.format('terminal',vrt_id, 'widget', widget_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.get(api, data=request.data, params=request.query_params, verify=True)

        request_response = self._manage_response(session, payload, response)      
        return Response(request_response)

    def process_resolve(self, request, vrt_id, widget_id, process_id, format=None):
        """
        """
        payload = self._merge_request_payload(request)

        # valiadte payload
        session = self._validate_payload(request, 'process', payload)

        url = '{0}/{1}/'.format('service', process_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.get(api, data=request.data, params=request.query_params, verify=True)

        request_response = self._manage_response(session, payload, response)      
        return Response(request_response)

    def _validate_payload(self, request, type_, payload):
        """
        """
        # create session (state = init)
        session = self._create_request_session(type_)

        # update payload with parent session id (from request which have initated excecution of widgets)
        parent_session = request.query_params.get('session', None)
        valid_parent_session = RequestSession.objects.filter(requestId=parent_session)

        payload.update({'parent_session':parent_session})
        
        # created trace for state=init
        session_trace = self._create_request_trace(session, 'init', payload)
        
        if not parent_session and not valid_parent_session:
            request_response = {'detail': 'session id missing.'}
            
            # created trace for failing request (no parent session sent with request)
            session_trace = self._create_request_trace(session, 'failed', payload, response=request_response)

            raise ValidationError(request_response)

        return session

    def _manage_response(self, session, payload, response):
        """
        """  
        request_response = dict()

        if response.json():
            request_response = response.json()

        request_response.update({'session':session.requestId})

        if response.status_code == requests.codes.ok:
            # update session
            self._update_request_session_state(session, 'succeeded')
            # create session trace
            self._create_request_trace(session, 'succeeded', payload, response=request_response)

        elif response.status_code == 400:
            # update session
            self._update_request_session_state(session, 'wait')
            # create session trace
            self._create_request_trace(session, 'wait', payload, response=request_response)            
        else:
            # update session
            self._update_request_session_state(session, 'failed')
            # create session trace
            self._create_request_trace(session, 'failed', payload, response=request_response)            

        return request_response