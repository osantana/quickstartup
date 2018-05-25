from django.template.loaders.app_directories import Loader as DjangoLoader
from django.template.utils import get_app_template_dirs


class Loader(DjangoLoader):
    def get_dirs(self):
        template_dirs = list(get_app_template_dirs('templates'))
        return tuple(reversed(template_dirs))

    def get_template_sources(self, template_name):
        return super().get_template_sources(template_name)
