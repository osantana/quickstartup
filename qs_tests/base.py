from pathlib import Path

from django.apps import apps
from django.test import TestCase

from quickstartup.qs_pages.bootstrap import bootstrap_website_pages

TEST_ROOT_DIR = Path(__file__).parent
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (
            str(TEST_ROOT_DIR / "templates"),
        ),
        'OPTIONS': {
            'debug': True,
            'context_processors': (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "quickstartup.context_processors.project_infos",
                "quickstartup.context_processors.project_settings",
            ),
        },
    },
]


class BaseTestCase(TestCase):
    def setUp(self):
        bootstrap_website_pages(apps)

    # noinspection PyPep8Naming
    def assertStatusCode(self, response, code):
        self.assertEquals(response.status_code, code,
                          "{} != {}\n{}".format(response.status_code, code, response.content))

    def get_mail_payloads(self, message):
        text = ""
        html = ""

        for payload in message.message().get_payload():
            if payload.get_content_type() == "text/plain":
                text = payload.as_string()
            if payload.get_content_type() == "text/html":
                html = payload.as_string()

        return text, html
