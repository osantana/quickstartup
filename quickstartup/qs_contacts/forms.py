# coding: utf-8


from django import forms
from django.utils.translation import ugettext_lazy as _
from djmail import template_mail
from ipware.ip import get_ip

from quickstartup.qs_core.antispam import AntiSpamField
from quickstartup.qs_core.widgets import EmailInput, PhoneInput
from quickstartup.settings_utils import get_configuration
from .models import Contact
from .signals import new_contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"), max_length=255)
    email = forms.EmailField(label=_("E-mail"), max_length=255, widget=EmailInput())
    phone = forms.CharField(label=_("Phone"), max_length=100, widget=PhoneInput(), required=False)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea(attrs={'rows': 5}))
    antispam = AntiSpamField()

    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "message", "antispam")

    def _send_contact_email(self, request, contact):
        context = {
            'request': request,
            'contact': contact,
            'project_name': get_configuration("QS_PROJECT_NAME"),
            'project_url': get_configuration("QS_PROJECT_URL"),
        }
        mails = template_mail.MagicMailBuilder()
        email = mails.new_contact(get_configuration("QS_PROJECT_CONTACT"), context,
                                  headers={"Reply-To": contact.email})
        email.send()

    def finish(self, request):
        contact = super().save(commit=False)
        contact.ip = get_ip(request)
        contact.save()
        self._send_contact_email(request, contact)
        new_contact.send(sender=self.__class__, contact=contact, request=request)
