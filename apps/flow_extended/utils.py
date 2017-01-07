"""
"""

from rest_framework import serializers

from requests import Request, Session
import six


class NoneSerializer(serializers.Serializer):
    """
    """
    pass

def service_rq(__s, method, headers, param, data, url):
    """
    """
    resp = {}

    rq = Request(
        method=method,
        url=url,
        params=param,
        data=data,
        headers=headers
    )
    rq = __s.prepare_request(rq)
    rs = __s.send(rq, stream=True)

    resp.update({
        'status':rs.status_code,
        'header':rs.headers,
        'raw':six.BytesIO(rs.content).getvalue()
    })

    return resp