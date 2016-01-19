# coding: utf-8
#
# Extract heavy logic from settings.py, manage.py and wsgi.py
#


import logging

from django.core.exceptions import ImproperlyConfigured


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        messages = []
        data = kwargs.get('extra', {})
        for key, value in sorted(data.items()):
            if "pass" in key:
                value = '*' * 6

            messages.append('{}={!r}'.format(key, value))
        return '{} {}'.format(msg, ', '.join(messages)), kwargs


def get_logger(name):
    return CustomAdapter(logging.getLogger(name), {})


def get_loggers(level, loggers):
    logging.addLevelName('DISABLED', logging.CRITICAL + 10)

    log_config = {
        'handlers': ['console'],
        'level': level,
    }

    if level == 'DISABLED':
        loggers = {'': {'handlers': ['null'], 'level': 'DEBUG', 'propagate': False}}
    else:
        loggers = {logger.strip(): log_config for logger in loggers}

    return loggers


def get_project_package(project_dir):
    if (project_dir / "project_name").exists():
        project_name = "project_name"
    else:
        settings_files = list(project_dir.glob("*/settings.py"))
        if len(settings_files) != 1:
            raise ImproperlyConfigured("settings.py not found or found more than one")
        project_name = settings_files[0].parent.name

    return project_name


def get_static_root(base_dir):
    try:
        from dj_static import Cling
    except ImportError:
        return str(base_dir / "static")

    return "staticfiles"


def get_media_root(base_dir):
    try:
        from dj_static import MediaCling
    except ImportError:
        return str(base_dir / "media")

    return "media"
