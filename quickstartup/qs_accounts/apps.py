from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    name = 'quickstartup.qs_accounts'
    verbose_name = _("Accounts")
