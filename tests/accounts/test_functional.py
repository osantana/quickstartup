import re
from unittest import mock
from urllib.parse import quote

import pytest
from django.core import mail
from django.core.signing import Signer
from django.test import override_settings
from django.urls import reverse

from ..base import check_form_error, check_redirects, get_mail_payloads

pytestmark = pytest.mark.django_db


def getmessage(response):
    for c in response.context:
        message = [m for m in c.get('messages')][0]
        if message:
            return message


def test_simple_reset_password(client, user):
    url = reverse("qs_accounts:password_reset")
    data = {"email": "test@example.com"}
    response = client.post(url, data, follow=True)
    assert response.status_code == 200

    message = getmessage(response)
    assert message.tags == "success"
    assert message.message == ("We've e-mailed you instructions for setting a new password to the "
                               "e-mail address you've submitted.")

    assert len(mail.outbox) == 1

    text, html = get_mail_payloads(mail.outbox[0])
    assert "Hi," in text
    assert "<h3>Hi,</h3>" in html

    reset_token = re.search(r"https://quickstartup.us(.*)$", text, re.MULTILINE)
    assert reset_token, "No reset token"

    reset_token_url = reset_token.groups()[0]
    client.get(reverse("qs_accounts:signin"))  # consume flash messages

    data = {"new_password1": "new-sekret", "new_password2": "new-sekret"}
    response = client.post(reset_token_url, data, follow=True)
    assert response.status_code == 200

    message = getmessage(response)
    assert message.tags == "success"
    assert message.message == "Password has been reset successfully."

    user = user.model.objects.get(email="test@example.com")  # reload user
    assert user.check_password("new-sekret"), "Password unchanged"


def test_reset_password_with_passwords_that_does_not_match(client, user):
    url = reverse("qs_accounts:password_reset")
    data = {"email": "test@example.com", "name": "John Doe"}
    response = client.post(url, data)

    reset_token_url = reverse("qs_accounts:password_reset_confirm",
                              kwargs={"reset_token": response.context["reset_token"]})

    data = {"new_password1": "sekret", "new_password2": "do-not-match"}
    response = client.post(reset_token_url, data)
    assert response.status_code == 200
    assert check_form_error(response, "form", "new_password2", ["The two password fields didn't match."])


@override_settings(AUTH_PASSWORD_VALIDATORS=[
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
])
def test_fail_reset_password_with_invalid_passwords(client, user):
    url = reverse("qs_accounts:password_reset")
    data = {"email": "test@example.com", "name": "John Doe"}
    response = client.post(url, data)

    reset_token_url = reverse("qs_accounts:password_reset_confirm",
                              kwargs={"reset_token": response.context["reset_token"]})

    data = {"new_password1": "123", "new_password2": "123"}
    response = client.post(reset_token_url, data)
    assert response.status_code == 200
    assert check_form_error(response, "form", "new_password1", ["This password is entirely numeric."])


def test_simple_reset_password_of_user_with_name(client, user):
    user.name = "John Doe"
    user.save()

    url = reverse("qs_accounts:password_reset")
    data = {"email": "test@example.com"}
    client.post(url, data)

    text, html = get_mail_payloads(mail.outbox[0])
    assert "Hi John Doe," in text
    assert "<h3>Hi John Doe,</h3>" in html


@mock.patch("quickstartup.qs_core.antispam.AntiSpamField.clean")
def test_full_signup_and_signin_signout_cycle(patched_clean, client, django_user_model):
    patched_clean.return_value = "1337"
    url = reverse("qs_accounts:signup")
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password1": "sekr3t",
        "password2": "sekr3t",
        "antispam": "1337",
    }

    # signup
    response = client.post(url, data, follow=True)
    assert response.status_code == 200

    # redirected to activation notice
    assert len(response.redirect_chain) == 1
    redirect_url = response.redirect_chain[0][0].replace("http://testserver", "")
    assert redirect_url == reverse("qs_accounts:signup_complete")

    # check user creation on database
    user = django_user_model.objects.get(email="john.doe@example.com")
    assert user.name, "John Doe"
    assert user.is_active is False
    assert user.is_staff is False
    assert user.is_superuser is False

    # check activation email
    text, html = get_mail_payloads(mail.outbox[0])
    assert "Hi John Doe," in text
    assert "<h3>Hi John Doe,</h3>" in html

    activation = re.search(r"https://quickstartup.us(.*)$", text, re.MULTILINE)
    assert activation, "No activation link in text email"

    activation_url = activation.groups()[0]
    assert activation_url in html

    # "click" on activation link
    response = client.get(activation_url, follow=True)
    assert response.status_code == 200
    assert len(response.redirect_chain) == 1

    # check redirection as logged user
    redirect_url = response.redirect_chain[0][0].replace("http://testserver", "")
    assert redirect_url == reverse("app:index")

    # logout
    response = client.get(reverse("qs_accounts:signout"), follow=True)
    assert response.status_code == 200
    assert len(response.redirect_chain) == 1

    redirect_url = response.redirect_chain[0][0].replace("http://testserver", "")
    assert redirect_url == reverse("qs_pages:index")


def test_fail_signup_password_doesnt_match(client):
    url = reverse("qs_accounts:signup")
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password1": "sekr3t",
        "password2": "oops!",
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert check_form_error(response, "form", "password2",
                            ["The two password fields didn't match."])


@override_settings(AUTH_PASSWORD_VALIDATORS=[
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
])
def test_fail_signup_invalid_password(client):
    url = reverse("qs_accounts:signup")
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password1": "123",  # invalid numeric-only password
        "password2": "123",
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert check_form_error(response, "form", "password1",
                            ["This password is entirely numeric."])


def test_change_password(logged_client, user):
    data = {
        "old_password": "secret",
        "new_password1": "sekret",
        "new_password2": "sekret",
    }

    response = logged_client.post(
        reverse("qs_accounts:password_change"),
        data,
        follow=True,
    )
    assert response.status_code == 200

    # refresh!
    user.refresh_from_db()
    assert user.check_password("sekret"), "Password not modified"


@override_settings(AUTH_PASSWORD_VALIDATORS=[
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
])
def test_fail_change_invalid_password(logged_client, user):
    data = {
        "old_password": "secret",
        "new_password1": "123",
        "new_password2": "123",
    }
    response = logged_client.post(reverse("qs_accounts:password_change"), data)
    assert response.status_code == 200
    assert check_form_error(response, "form", "new_password1",
                            ["This password is entirely numeric."])

    user.refresh_from_db()  # refresh
    assert user.check_password("secret"), "Password modified"


def test_change_email(logged_client, user):
    data = {
        "new_email": "new@example.com",
    }

    response = logged_client.post(reverse("qs_accounts:email_change"), data, follow=True)
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.email == "test@example.com"
    assert user.new_email == "new@example.com"

    # check activation email
    assert len(mail.outbox) == 1

    text, html = get_mail_payloads(mail.outbox[0])
    assert "Hi," in text
    assert "<h3>Hi,</h3>" in html

    change = re.search(r"https://quickstartup.us(.*)$", text, re.MULTILINE)
    assert change, "No activation link in text email"

    change_url = change.groups()[0]
    assert change_url in html

    # "click" on change e-mail confirmation link
    response = logged_client.get(change_url, follow=True)
    assert response.status_code == 200
    assert len(response.redirect_chain) == 1

    message = getmessage(response)
    assert message.tags == "success"
    assert message.message == "New e-mail has been successfully configured."

    user.refresh_from_db()
    assert user.email == "new@example.com"
    assert user.new_email is None


def test_fail_set_email_as_anonymous(client, user):
    # not logged!
    response = client.post(reverse("qs_accounts:email_change"), {"new_email": "new@example.com"})

    url = "%s?next=%s" % (reverse("qs_accounts:signin"), reverse("qs_accounts:email_change"))
    assert check_redirects(response, url)

    user.refresh_from_db()
    assert user.new_email is None


def test_fail_confirm_email_as_anonymous(logged_client, user):
    logged_client.post(reverse("qs_accounts:email_change"), {"new_email": "new@example.com"})
    logged_client.logout()

    text, html = get_mail_payloads(mail.outbox[0])
    change = re.search(r"https://quickstartup.us(.*)$", text, re.MULTILINE)
    change_url = change.groups()[0]

    response = logged_client.get(change_url)
    url = "%s?next=%s" % (reverse("qs_accounts:signin"), quote(change_url))
    assert check_redirects(response, url)

    user.refresh_from_db()
    assert user.email == 'test@example.com'
    assert user.new_email == 'new@example.com'


def test_fail_confirm_email_with_invalid_token(logged_client, user):
    response = logged_client.post(
        reverse("qs_accounts:email_change"),
        {"new_email": "new@example.com"},
        follow=True)
    assert response.status_code == 200

    text, html = get_mail_payloads(mail.outbox[0])
    change = re.search(r"https://quickstartup.us(.*)$", text, re.MULTILINE)

    change_url = change.groups()[0][:-2] + "/"  # make token signature invalid

    response = logged_client.get(change_url, follow=True)
    assert response.status_code == 200
    assert len(response.redirect_chain) == 1

    message = getmessage(response)
    assert message.tags == "danger"
    assert message.message == "Invalid e-mail configuration token."

    user.refresh_from_db()
    assert user.email == 'test@example.com'
    assert user.new_email == 'new@example.com'


def test_fail_confirm_email_with_invalid_username(logged_client, user):
    response = logged_client.post(reverse("qs_accounts:email_change"), {"new_email": "new@example.com"}, follow=True)
    assert response.status_code == 200

    signer = Signer()
    activation_key = signer.sign("invalid@example.com")
    change_url = reverse("qs_accounts:email_change_confirmation", kwargs={"activation_key": activation_key})

    response = logged_client.get(change_url, follow=True)
    assert response.status_code == 200
    assert len(response.redirect_chain) == 1

    message = getmessage(response)
    assert message.tags == "danger"
    assert message.message == "E-mail not found."

    user.refresh_from_db()
    assert user.email == 'test@example.com'
    assert user.new_email == 'new@example.com'
