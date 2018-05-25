from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ContactConfig(AppConfig):
    name = 'quickstartup.qs_contacts'
    verbose_name = _("Contacts")
