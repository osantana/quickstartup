# coding: utf-8


from django.db import IntegrityError
from django.test import TestCase

from quickstartup.qs_contacts.models import Contact


class ContactTestCase(TestCase):
    def test_basic_contact(self):
        contact = Contact.objects.create(name="John Doe",
                                         ip="8.8.8.8",
                                         email="john.doe@example.com",
                                         phone="(41) 3076-0406",
                                         message="Hello World!")

        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.ip, "8.8.8.8")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.phone, "(41) 3076-0406")
        self.assertEqual(contact.message, "Hello World!")
        self.assertEqual(str(contact), "John Doe <john.doe@example.com>")

    def test_fail_contact_missing_name(self):
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                    ip="8.8.8.8",
                    email="john.doe@example.com",
                    phone="(41) 3076-0406",
                    message="Hello World!",
            )

        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                    ip="8.8.8.8",
                    name="John Doe",
                    phone="(41) 3076-0406",
                    message="Hello World!",
            )

        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                    ip="8.8.8.8",
                    name="John Doe",
                    email="john.doe@example.com",
                    phone="(41) 3076-0406",
            )
