from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .utils import fail, success


class CustomJSONRenderer(JSONRenderer):
    """
    Custom JSON renderer
    """

    def render(self, data, accepted_media_type=None, renderer_context: dict | None = None) -> bytes:
        """
        :param data: response data
        :param accepted_media_type: accepted media type
        :param renderer_context: renderer context
        :return: json response

        """
        response: Response = renderer_context.get('response')
        if response.status_code in range(200, 400):
            return super().render(success(data), accepted_media_type, renderer_context)
        return super().render(fail(data), accepted_media_type, renderer_context)
