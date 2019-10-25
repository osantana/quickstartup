from unittest import mock

import pytest
from django.core import mail
from django.urls import reverse

from quickstartup.qs_contacts.models import Contact
from ..base import check_form_error, check_template_used

pytestmark = pytest.mark.django_db


@mock.patch("quickstartup.qs_core.antispam.AntiSpamField.clean")
def test_send_contact(patched_clean, client):
    patched_clean.return_value = "1337"
    data = {
        "name": u"John Doe",
        "email": u"john@doe.com",
        "phone": u"+1 55 555-1234",
        "message": u"Hello World!",
        "antispam": u"1337",
    }

    url = reverse("qs_contacts:contact")
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert check_template_used(response, "contacts/contact.html")
    assert len(mail.outbox) == 1

    email = mail.outbox[0]
    contact = Contact.objects.first()

    assert email.extra_headers["Reply-To"] == 'john@doe.com'
    assert "contact@quickstartup.us" in email.to
    assert email.subject == u'New Contact from Django Quickstartup'
    assert u"Contact From: John Doe <john@doe.com>" in email.body
    assert u"Phone: +1 55 555-1234" in email.body
    assert u"Message:\n\n    Hello World!" in email.body
    assert "https://quickstartup.us/admin/qs_contacts/contact/{}/change/".format(contact.id) in email.body
    assert "IP: 127.0.0.1" in email.body

    assert contact.name == u"John Doe"
    assert contact.email == u"john@doe.com"
    assert contact.phone == u"+1 55 555-1234"
    assert contact.message == u"Hello World!"
    assert contact.status == "N"
    assert contact.ip == "127.0.0.1"


def test_fail_antispam(client):
    data = {
        "name": u"John Doe",
        "email": u"john@doe.com",
        "phone": u"+1 55 555-1234",
        "message": u"Hello World!",
        "antispam": u"1337",
    }

    url = reverse("qs_contacts:contact")
    response = client.post(url, data, follow=True)
    assert check_form_error(response, 'form', 'antispam', u'You need to enable JavaScript to complete this form.')


def test_access_an_existent_url(client):
    response = client.get("/contact/")
    assert response.status_code == 200
    assert check_template_used(response, "contacts/contact.html")
