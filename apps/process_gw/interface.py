"""
every incoming request to call a process will be validated here
like its end-point, headers, authentication, payload etc
"""

from apps.resource.models import Resource

from routes import Mapper
map = Mapper()
# map.connect(None, "/error/{action}/{id}", controller="error")
# map.connect("home", "/", controller="main", action="index")

# # Match a URL, returns a dict or None if no match
# result = map.match('/error/myapp/4')
# result == {'controller': 'error', 'action': 'myapp', 'id': '4'}


def spilt_endpoint(url):
    """
    """
    return url.split('.in/')

def valiadte_request_path(requested_path, resource_request_path):
    """
    for mathicng routers we have used repo routes
    """
    map.connect("resource_api", resource_request_path, controller="main", action="index")
    asqwe = map.match(requested_path)
    return asqwe

def validate_endpoint(request, resource, url):
    """
    """
    # resource = None
    # try:
    #     resource = Resource.objects.get(resource_end_point=url)
    # except:
    #     return {'error': True, 'code': 400, 'detail': 'Wrong Resource endpoint', 'api':None} 


    # split url so taht rtequested resquest path an dsaved resource path can be matched
    domain, requested_path = spilt_endpoint(url)

    if not valiadte_request_path(requested_path, resource.request_path):
        return {'error': True, 'code': 404, 'detail': 'Wrong Resource endpoint', 'api':None} 

    return {'error': False, 'code': 200, 'detail': 'success', 'api':requested_path} 

