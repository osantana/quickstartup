# coding: utf-8


from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from ..messages import send_contact_mail

CONTACT_STATUS = (
    ("N", _("New")),
    ("O", _("Ongoing")),
    ("R", _("Resolved")),
    ("C", _("Closed")),
    ("I", _("Invalid")),
)


class Contact(models.Model):
    status = models.CharField(_("status"), max_length=1, choices=CONTACT_STATUS, default="N")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"), max_length=255)
    phone = models.CharField(_("phone"), max_length=100, blank=True)
    message = models.TextField(_("message"))
    ip = models.GenericIPAddressField(_("contact ip"))

    @property
    def admin_url(self):
        return reverse("admin:contacts_contact_change", args=(self.pk,))

    def __str__(self):
        return "{} <{}>".format(self.name, self.email)


post_save.connect(send_contact_mail, Contact, dispatch_uid="quickstartup.contacts")
