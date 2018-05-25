from unittest import mock

from django.core import mail
from django.urls import reverse

from quickstartup.qs_contacts.models import Contact
from ..base import BaseTestCase, TEST_ROOT_DIR

TEMPLATE_DIRS = (
    str(TEST_ROOT_DIR / "templates"),
)


class ContactTest(BaseTestCase):
    @mock.patch("quickstartup.qs_core.antispam.AntiSpamField.clean")
    def test_send_contact(self, patched_clean):
        patched_clean.return_value = "1337"
        data = {
            "name": u"John Doe",
            "email": u"john@doe.com",
            "phone": u"+1 55 555-1234",
            "message": u"Hello World!",
            "antispam": u"1337",
        }

        url = reverse("qs_contacts:contact")
        response = self.client.post(url, data, follow=True)
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed(response, "contacts/contact.html")
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        contact = Contact.objects.first()

        self.assertEquals(email.extra_headers["Reply-To"], 'john@doe.com')
        self.assertIn("contact@quickstartup.us", email.to)
        self.assertEqual(email.subject, u'New Contact from Django Quickstartup')
        self.assertIn(u"Contact From: John Doe <john@doe.com>", email.body)
        self.assertIn(u"Phone: +1 55 555-1234", email.body)
        self.assertIn(u"Message:\n\n    Hello World!", email.body)
        self.assertIn("https://quickstartup.us/admin/qs_contacts/contact/{}/change/".format(contact.id), email.body)
        self.assertIn("IP: 127.0.0.1", email.body)

        self.assertEqual(contact.name, u"John Doe")
        self.assertEqual(contact.email, u"john@doe.com")
        self.assertEqual(contact.phone, u"+1 55 555-1234")
        self.assertEqual(contact.message, u"Hello World!")
        self.assertEqual(contact.status, "N")
        self.assertEqual(contact.ip, "127.0.0.1")

    def test_fail_antispam(self):
        data = {
            "name": u"John Doe",
            "email": u"john@doe.com",
            "phone": u"+1 55 555-1234",
            "message": u"Hello World!",
            "antispam": u"1337",
        }

        url = reverse("qs_contacts:contact")
        response = self.client.post(url, data, follow=True)
        self.assertFormError(response, 'form', 'antispam', u'You need to enable JavaScript to complete this form.')

    def test_access_an_existent_url(self):
        response = self.client.get("/contact/")
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed(response, "contacts/contact.html")
