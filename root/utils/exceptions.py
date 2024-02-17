from rest_framework.exceptions import APIException
from rest_framework.response import Response


def exception_handler(exc: Exception, **context) -> Response:
    if isinstance(exc, APIException):
        return Response(exc.detail, status=exc.status_code)
    return Response(str(exc), status=500)
