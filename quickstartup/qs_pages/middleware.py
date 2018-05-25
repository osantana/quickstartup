from django.conf import settings
from django.http import Http404

from .views import website_page


def website_page_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code != 404:
            return response

        # noinspection PyBroadException
        try:
            return website_page(request, request.path_info)
        except Http404:
            return response
        except Exception as ex:
            if settings.DEBUG:
                raise
            return response

    return middleware
