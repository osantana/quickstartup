# coding: utf-8


from datetime import datetime, timedelta
from hashlib import sha1

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

ERROR_MESSAGE = _(u'You need to enable JavaScript to complete this form.')


def get_antispam_tokens():
    date_format = "%Y-%m-%d"

    today = datetime.utcnow().strftime(date_format)
    yesterday = (datetime.utcnow() - timedelta(1)).strftime(date_format)

    secrets = (
        settings.SECRET_KEY + today,
        settings.SECRET_KEY + yesterday,
    )

    return [sha1(secret.encode("ascii")).hexdigest() for secret in secrets]


class AntiSpamWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        output = '''<script>document.write('<input type="hidden" name="antispam" value="%s"/>')</script>''' % (get_antispam_tokens()[0],)
        return mark_safe(output)


class AntiSpamField(forms.CharField):
    widget = AntiSpamWidget
    default_error_messages = {
        'required': ERROR_MESSAGE,
    }

    def clean(self, value):
        value = super(AntiSpamField, self).clean(value)

        if value not in get_antispam_tokens():
            raise forms.ValidationError(ERROR_MESSAGE)
