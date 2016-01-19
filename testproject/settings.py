# coding: utf-8


from pathlib import Path

from django.contrib.messages import constants as message_constants

from quickstartup.settings_utils import (get_project_package, get_loggers, get_static_root, get_media_root)

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
        'NAME': str(PROJECT_DIR / 'quickstartup.db'),
    }
}

# Email
DEFAULT_FROM_EMAIL = PROJECT_CONTACT
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "./app-messages"

# Security & Signup/Signin
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "SEKRET-KEY"
AUTH_USER_MODEL = "qs_accounts.User"
LOGIN_REDIRECT_URL = "app:index"
LOGIN_URL = "qs_accounts:signin"
ACCOUNT_ACTIVATION_DAYS = 7

# REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.
# REGISTRATION_OPEN = True
# REGISTRATION_FORM = "quickstartup.qs_accounts.forms.SignupForm"

ADMIN_URL = "admin"  # empty to disable admin URLs

AUTHENTICATION_BACKENDS = (
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
    'quickstartup.qs_website.middleware.WebsitePageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party libs
    'widget_tweaks',

    # Quick Startup Apps
    'quickstartup.qs_core',
    'quickstartup.qs_accounts',
    'quickstartup.qs_website',
    'quickstartup.qs_contacts',
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

MESSAGE_TAGS = {message_constants.ERROR: 'danger'}
