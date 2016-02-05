# coding: utf-8


from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _


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
    email = models.EmailField(_("e-mail"), max_length=255, blank=False, null=False)
    phone = models.CharField(_("phone"), max_length=100, blank=True)
    message = models.TextField(_("message"), blank=False, null=False)
    ip = models.GenericIPAddressField(_("contact ip"))

    @property
    def admin_url(self):
        return reverse("admin:qs_contacts_contact_change", args=(self.pk,))

    def __str__(self):
        return "{} <{}>".format(self.name, self.email)

    def save(self, *args, **kwargs):
        if not self.name:
            raise IntegrityError("Missing name")

        if not self.email:
            raise IntegrityError("Missing email")

        if not self.message:
            raise IntegrityError("Missing message")

        super().save(*args, **kwargs)
