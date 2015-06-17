import sys

from pathlib import Path

TEST_DIR = Path(__file__).absolute().parents[1]
FRONTEND_DIR = TEST_DIR / "frontend"

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="quickstartup.urls",
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'widget_tweaks',
            'registration',
            'social.apps.django_app.default',
            "quickstartup.core",
            "quickstartup.website",
            "quickstartup.accounts",
            "quickstartup.contacts",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.gzip.GZipMiddleware',
            'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
            'quickstartup.website.middleware.WebsitePageMiddleware',
        ),
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': (
                    str(FRONTEND_DIR / "templates"),
                ),
                'OPTIONS': {
                    'debug': True,
                    'loaders': (
                        'django.template.loaders.filesystem.Loader',
                        'quickstartup.template_loader.Loader'
                    ),
                    'context_processors': (
                        "django.contrib.auth.context_processors.auth",
                        "django.core.context_processors.debug",
                        "django.core.context_processors.i18n",
                        "django.core.context_processors.media",
                        "django.core.context_processors.static",
                        "django.core.context_processors.request",
                        "django.core.context_processors.tz",
                        "django.contrib.messages.context_processors.messages",
                        "social.apps.django_app.context_processors.backends",
                        "social.apps.django_app.context_processors.login_redirect",
                        "quickstartup.context_processors.project_infos",
                        "quickstartup.context_processors.project_settings",
                    ),
                },
            },
        ],
        FRONTEND_DIR = TEST_DIR / "frontend",
        AUTH_USER_MODEL = "accounts.User",
        LOGIN_REDIRECT_URL = "app:index",
        LOGIN_URL = "qs_accounts:signin",
        ACCOUNT_ACTIVATION_DAYS = 7,
        REGISTRATION_AUTO_LOGIN = True,
        REGISTRATION_OPEN = True,
        REGISTRATION_FORM = "quickstartup.accounts.forms.SignupForm",
        SOCIAL_AUTH_LOGIN_REDIRECT_URL = "app:index",
        SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy',
        SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage',
        SOCIAL_AUTH_USER_MODEL = "accounts.User",
        SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True,
        SOCIAL_AUTH_LOGIN_ERROR_URL = '/accounts/social-auth-errors/',
        SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email'],
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
        ),
        PROJECT_NAME="Django Quickstartup",
        PROJECT_DOMAIN="example.com",
        PROJECT_CONTACT="contact@example.com",
        STATIC_URL="/static/",
        ADMIN_URL="admin",
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

    from django_nose import NoseTestSuiteRunner
except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
