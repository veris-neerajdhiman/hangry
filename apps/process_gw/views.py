
from django.conf import settings

from rest_framework import viewsets, status, serializers
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView


from apps.process_gw.models import RequestSession, RequestTrace
from apps.process_gw import interface
from apps.api_gw.widgets.models import Widgets

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
            'post':request.data
            })
        return payload

    def _validate_request(self, request):
        """
        """
        session = request.data.get('session', None) 
        valid_session = RequestSession.objects.filter(requestId=session)

        if not session or not valid_session:
            return {'halt':False, 'session':self._create_request_session('vrt')}

        request_trace = RequestTrace.objects.get(request=valid_session[0], state=valid_session[0].state)

        return {'halt':True, 'trace':request_trace}
              
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

    def _create_request_trace(self, session, parent_session, state, payload, response=None):
        """
        """
        initial_trace_data ={
            'request':session,
            'state':state,
            'payload':payload,
            'parent_request':parent_session,
            }

        if response:
            initial_trace_data.update({'response':response})

        try:
            return RequestTrace.objects.get(request=session, state=state, parent_request=parent_session)
        except:
            pass
        return RequestTrace.objects.create(**initial_trace_data)

    def vrt_resolve(self, request, vrt_id, format=None):
        """
        """
        vrt_request = self._validate_request(request)
        if vrt_request.get('halt') is True:
            return Response(vrt_request.get('trace').response, status=status.HTTP_202_ACCEPTED)


        payload = self._merge_request_payload(request)

        # create session (state = init)
        session = vrt_request.get('session')

        session_trace = self._create_request_trace(session, session, 'init', payload)

        # update session (state=in process)
        self._update_request_session_state(session, 'inprocess')
        session_trace = self._create_request_trace(session, session, 'inprocess', payload)

        # call API g/w
        url = '{0}/{1}/'.format('terminal', vrt_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.post(api, data=request.data, params=request.query_params, verify=True)

        request_response = self._manage_response(session, session, payload, response)      
        return Response(request_response)

    def widget_resolve(self, request, vrt_id, widget_id, format=None):
        """
        """
        payload = self._merge_request_payload(request)

        # valiadte payload
        valid_request = self._validate_payload(request, 'widget', payload)
        session = valid_request.get('session')
        parent_session = valid_request.get('parent_session')

        # update session (state=in process)
        self._update_request_session_state(session, 'inprocess')
        session_trace = self._create_request_trace(session, parent_session, 'inprocess', payload)

        # call API g/w
        url = '{0}/{1}/{2}/{3}/'.format('terminal',vrt_id, 'widget', widget_id)
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.get(api, data=request.data, params=request.query_params, verify=True)

        request_response = self._manage_response(session, parent_session, payload, response)      
        return Response(request_response)

    def process_resolve(self, request, vrt_id, widget_id, process_id, format=None):
        """
        """
        # TODO : we need to find out a better way to call rtesource endpoints
        # get widget Resource and hit its API
        widget = Widgets.objects.get(pk=widget_id)
        endpoint = widget.resource.resource_end_point.replace("{key}", process_id)
        req = interface.validate_endpoint(request, widget.resource, endpoint)

        if req.get('error') is True:
            return Response(req)

        payload = self._merge_request_payload(request)

        # if request
        process_request = request.query_params.get('request')
        valid_process_request = RequestTrace.objects.filter(request__requestId=process_request, state='wait')
        if not valid_process_request:

            # valiadte payload
            valid_request = self._validate_payload(request, 'process', payload)
            session = valid_request.get('session')
            parent_session = valid_request.get('parent_session')

            # update session (state=in process)
            self._update_request_session_state(session, 'inprocess')
            session_trace = self._create_request_trace(session, parent_session, 'inprocess', payload)       
        else:
            session = valid_process_request[0].request
            parent_session = valid_process_request[0].parent_request

        url = req.get('api')
        api = '{0}{1}/{2}'.format('http://', request.get_host(), url)
        response = requests.post(api, data=request.data, params=request.query_params, verify=True)

        request_response = self._manage_response(session, parent_session, payload, response)      
        return Response(request_response)

    def _validate_payload(self, request, type_, payload):
        """
        """
        # create session (state = init)
        session = self._create_request_session(type_)

        # update payload with parent session id (from request which have initated excecution of widgets)
        parent_session = request.data.get('session', None)
        valid_parent_session = RequestSession.objects.filter(requestId=parent_session)

        payload.update({'parent_session':parent_session})
        
        if not parent_session or not valid_parent_session:
            request_response = {'detail': 'session id missing.'}


            # # created trace for failing request (no parent session sent with request)
            # session_trace = self._create_request_trace(session, valid_parent_session[0], 'failed', payload, response=request_response)

            raise ValidationError(request_response)

        # created trace for state=init
        session_trace = self._create_request_trace(session, valid_parent_session[0], 'init', payload)  

        return {'session':session, 'parent_session':valid_parent_session[0]}

    def _manage_response(self, session, parent_session, payload, response):
        """
        """
        request_response = dict()
        if response.json():
            request_response = response.json()

        request_response.update({'session':str(session.requestId)})

        if response.status_code == requests.codes.ok:
            # update session
            self._update_request_session_state(session, 'succeeded')
            # create session trace
            self._create_request_trace(session, parent_session, 'succeeded', payload, response=request_response)

        elif response.status_code == 400:
            # update session
            self._update_request_session_state(session, 'wait')
            # create session trace
            self._create_request_trace(session, parent_session, 'wait', payload, response=request_response)            
        else:
            # update session
            self._update_request_session_state(session, 'failed')
            # create session trace
            self._create_request_trace(session, parent_session, 'failed', payload, response=request_response)            

        return request_response