# coding: utf-8


from django.template.loaders.app_directories import Loader as DjangoLoader
from django.template.utils import get_app_template_dirs


class Loader(DjangoLoader):
    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = list(get_app_template_dirs('templates'))
            template_dirs = tuple(reversed(template_dirs))
        return super().get_template_sources(template_name, template_dirs=template_dirs)
