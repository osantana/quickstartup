from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactConfig(AppConfig):
    name = 'quickstartup.qs_contacts'
    verbose_name = _("Contacts")
