import pytest
from django.db import IntegrityError

from quickstartup.qs_contacts.models import Contact

pytestmark = pytest.mark.django_db


def test_basic_contact():
    contact = Contact.objects.create(name="John Doe",
                                     ip="8.8.8.8",
                                     email="john.doe@example.com",
                                     phone="(41) 3076-0406",
                                     message="Hello World!")

    assert contact.name == "John Doe"
    assert contact.ip == "8.8.8.8"
    assert contact.email == "john.doe@example.com"
    assert contact.phone == "(41) 3076-0406"
    assert contact.message == "Hello World!"
    assert str(contact) == "John Doe <john.doe@example.com>"


def test_fail_contact_missing_name():
    with pytest.raises(IntegrityError):
        Contact.objects.create(
            ip="8.8.8.8",
            email="john.doe@example.com",
            phone="(41) 3076-0406",
            message="Hello World!",
        )

    with pytest.raises(IntegrityError):
        Contact.objects.create(
            ip="8.8.8.8",
            name="John Doe",
            phone="(41) 3076-0406",
            message="Hello World!",
        )

    with pytest.raises(IntegrityError):
        Contact.objects.create(
            ip="8.8.8.8",
            name="John Doe",
            email="john.doe@example.com",
            phone="(41) 3076-0406",
        )
