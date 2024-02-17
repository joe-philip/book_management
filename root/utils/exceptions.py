from django.http.response import Http404
from rest_framework.exceptions import APIException
from rest_framework.response import Response


def exception_handler(exc: Exception, *args, **context) -> Response:
    if isinstance(exc, APIException):
        return Response(exc.detail, status=exc.status_code)
    if isinstance(exc, Http404):
        return Response('Object not found', status=404)
    return Response(str(exc), status=500)
