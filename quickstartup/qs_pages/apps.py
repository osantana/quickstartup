from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PagesConfig(AppConfig):
    name = 'quickstartup.qs_pages'
    verbose_name = _("Website Pages")
