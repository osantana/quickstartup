# coding: utf-8


from pathlib import Path

from quickstartup.settings_utils import (get_project_package, get_loggers,
                                         get_site_id, get_static_root, get_media_root)


# Project Structure
BASE_DIR = Path(__file__).absolute().parents[2]
PROJECT_DIR = Path(__file__).absolute().parents[1]
FRONTEND_DIR = PROJECT_DIR / "frontend"


# Project Info
PROJECT_NAME = "Django Quickstartup"
PROJECT_CONTACT = "contact@quickstartup.us"
PROJECT_DOMAIN = "quickstartup.us"


# Debug & Development
DEBUG = True


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/quickstartup.db',
    }
}


# Email
DEFAULT_FROM_EMAIL = PROJECT_CONTACT

# Security & Signup/Signin
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "SEKRET-KEY"
AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = "app:index"
LOGIN_URL = "qs_accounts:signin"
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.
REGISTRATION_OPEN = True
REGISTRATION_FORM = "quickstartup.accounts.forms.SignupForm"
ADMIN_URL = "admin"  # empty to disable admin URLs

# Social authentication
SOCIAL_AUTH_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_LOGIN_ERROR_URL = '/accounts/social-auth-errors/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']  # If user already exists, do not override his email

# This should be set properly by each backend (check the documentation)
# SOCIAL_AUTH_TWITTER_KEY = ''
# SOCIAL_AUTH_TWITTER_SECRET = ''
# SOCIAL_AUTH_GOOGLE_OAUTH_KEY = ''
# SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = ''

AUTHENTICATION_BACKENDS = (
    # 'social.backends.twitter.TwitterOAuth',
    # 'social.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)


# i18n & l10n
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("en", u"English"),
    ("pt-br", u"Português (Brasil)"),
)

LOCALE_PATHS = (
    str(PROJECT_DIR / "locale"),
)


# Miscelaneous
_project_package = get_project_package(PROJECT_DIR)
ROOT_URLCONF = "{}.urls".format(_project_package)
WSGI_APPLICATION = "{}.wsgi.application".format(_project_package)
SITE_ID = get_site_id(PROJECT_DOMAIN, PROJECT_NAME)


# Media & Static
MEDIA_URL = "/media/"
MEDIA_ROOT = get_media_root(BASE_DIR)

STATIC_URL = "/static/"
STATIC_ROOT = get_static_root(BASE_DIR)
STATICFILES_DIRS = (
    str(FRONTEND_DIR / "static"),
)


# Templates
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
]


# Application
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
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # 3rd party libs
    'widget_tweaks',
    'registration',
    'social.apps.django_app.default',

    # Quick Startup Apps
    'quickstartup.core',
    'quickstartup.accounts',
    'quickstartup.website',
    'quickstartup.contacts',
)


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': get_loggers("INFO", ""),
}
