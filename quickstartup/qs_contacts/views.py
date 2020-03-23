from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from quickstartup.settings_utils import get_object_from_configuration
from .forms import ContactForm


class ContactView(CreateView):
    template_name = 'contacts/contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse("qs_contacts:contact")

    def get_form_class(self):
        return get_object_from_configuration("QS_CONTACT_FORM")

    def form_valid(self, form):
        form.finish(self.request)
        messages.success(self.request, _("Your message was sent successfully!"))
        return super().form_valid(form)
