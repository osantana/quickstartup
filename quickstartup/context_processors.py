# coding: utf-8


from django.conf import settings

from quickstartup.settings_utils import get_configuration


# noinspection PyUnusedLocal
def project_infos(request):
    return {
        "PROJECT_NAME": get_configuration("QS_PROJECT_NAME"),
        "PROJECT_DOMAIN": get_configuration("QS_PROJECT_DOMAIN"),
        "PROJECT_CONTACT": get_configuration("QS_PROJECT_CONTACT"),
    }


# noinspection PyUnusedLocal
def project_settings(request):
    return {"PROJECT_SETTINGS": settings}
