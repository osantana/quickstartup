# coding: utf-8


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WebsiteConfig(AppConfig):
    name = 'quickstartup.qs_website'
    verbose_name = _("Website Pages")
