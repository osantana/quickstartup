# coding: utf-8


from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, override_settings

from quickstartup.accounts.templatetags.get_social_backends import get_social_backends
from quickstartup.accounts.utils import get_social_message_errors

from tests.base import BaseTestCase


class SocialAuthErrorsViewTest(BaseTestCase):
    def setUp(self):
        super(SocialAuthErrorsViewTest, self).setUp()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(email="test@example.com", password="secret")

    def test_redirection_user_not_authenticated(self):
        response = self.client.get(reverse('qs_accounts:social-auth-errors'))
        self.assertStatusCode(response, 302)
        self.assertIn(resolve_url(reverse('qs_accounts:signup')), response['location'])

    def test_redirection_user_not_authenticated_keep_querystring(self):
        response = self.client.get(reverse('qs_accounts:social-auth-errors') + '?foo=bar')
        self.assertStatusCode(response, 302)
        self.assertIn(resolve_url(reverse('qs_accounts:signup')), response['location'])
        self.assertIn('?foo=bar', response['location'])

    def test_redirection_user_authenticated(self):
        logged = self.client.login(username=self.user.email, password='secret')
        self.assertTrue(logged)

        response = self.client.get(reverse('qs_accounts:social-auth-errors'))
        self.assertStatusCode(response, 302)
        self.assertIn(resolve_url(reverse('qs_accounts:profile-social')), response['location'])


class GetSocialMessageErrorsTest(BaseTestCase):
    def test_get_social_message_errors_empty(self):
        request = RequestFactory().get('/')
        msgs = get_social_message_errors(request)
        self.assertEquals(msgs, [])

    def test_get_social_message_errors(self):
        request = RequestFactory().get('/')
        # RequestFactory is very limited, so we have to tweak this request in order to work with
        # messages middleware
        request.session = {}
        request._messages = FallbackStorage(request)

        messages.add_message(request, messages.ERROR, 'test')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0].message, 'test')
        self.assertEquals(msgs[0].level, messages.ERROR)

    def test_get_social_message_errors_with_other_messages(self):
        request = RequestFactory().get('/')
        request.session = {}
        request._messages = FallbackStorage(request)

        messages.add_message(request, messages.ERROR, 'test')
        messages.add_message(request, messages.INFO, 'info')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0].message, 'test')
        self.assertEquals(msgs[0].level, messages.ERROR)

    def test_get_social_message_errors_querystring(self):
        request = RequestFactory().get('/?message=test-query-string')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0], 'test-query-string')

    def test_get_social_message_errors_ignore_querystring(self):
        request = RequestFactory().get('/?message=test-query-string')
        request.session = {}
        request._messages = FallbackStorage(request)

        messages.add_message(request, messages.ERROR, 'test')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0].message, 'test')
        self.assertEquals(msgs[0].level, messages.ERROR)


@override_settings(AUTHENTICATION_BACKENDS=('social.backends.twitter.TwitterOAuth',
                                            'django.contrib.auth.backends.ModelBackend'))
class AccountTemplateTagsTest(BaseTestCase):
    def test_get_backends(self):
        backends = get_social_backends()
        self.assertTrue('twitter' in backends)
        self.assertEquals(len(backends), 1)
