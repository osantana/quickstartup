# coding: utf-8


from django.core import mail
from django.core.mail import SafeMIMEText
from django.test import override_settings
from django.contrib.auth import get_user_model

from tests.base import BaseTestCase, TEMPLATES
from quickstartup.messages import send_transaction_mail

UserModel = get_user_model()


@override_settings(TEMPLATES=TEMPLATES)
class MessageTestCase(BaseTestCase):
    def test_multipart_messages(self):
        user = UserModel.objects.create_user()
        send_transaction_mail(user, "test-mail-multipart")
        text, html = self.get_mail_payloads(mail.outbox[0])
        self.assert_(text, "test-mail-multipart.txt")
        self.assert_(html, "test-mail-multipart.html")

    def test_text_only_messages(self):
        user = UserModel.objects.create_user()
        send_transaction_mail(user, "test-mail-text-only")

        message = mail.outbox[0]
        for payload in message.message().get_payload():
            if isinstance(payload, SafeMIMEText) and payload.get_content_type() != "text/plain":
                self.fail("Text only message with HTML payload")
