from pathlib import Path

from django.test import SimpleTestCase

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


def get_mail_payloads(message):
    text = ""
    html = ""

    for payload in message.message().get_payload():
        if payload.get_content_type() == "text/plain":
            text = payload.as_string()
        if payload.get_content_type() == "text/html":
            html = payload.as_string()

    return text, html


def check_form_error(response, form_name, field, errors, msg_prefix=''):
    test_case = SimpleTestCase()
    test_case.assertFormError(response, form_name, field, errors, msg_prefix)
    return True


def check_redirects(response, expected_url):
    test_case = SimpleTestCase()
    test_case.assertRedirects(response, expected_url=expected_url)
    return True


def check_template_used(response, template_name):
    test_case = SimpleTestCase()
    test_case.assertTemplateUsed(response, template_name=template_name)
    return True


def check_contains(response, text):
    test_case = SimpleTestCase()
    test_case.assertContains(response, text=text)
    return True


def check_in_html(needle, haystack):
    test_case = SimpleTestCase()
    test_case.assertInHTML(needle, haystack)
    return True
