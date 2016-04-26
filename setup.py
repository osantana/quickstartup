#!/usr/bin/env python
# coding: utf-8


import os
import re

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

here = os.path.abspath(os.path.dirname(__file__))

version = "0.0.0"
with open(os.path.join(here, "CHANGES.rst")) as changes:
    for line in changes:
        version = line.strip()
        if re.search('^[0-9]+\.[0-9]+(\.[0-9]+)?$', version):
            break


class VersionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    # noinspection PyMethodMayBeStatic
    def run(self):
        print(version)


readme = open('README.rst').read()
history = open('CHANGES.rst').read().replace('.. :changelog:', '')

setup(
    name='quickstartup',
    version=version,
    description="""Quickstartup package used by Quickstartup Template""",
    long_description=readme + '\n\n' + history,
    author='Osvaldo Santana Neto',
    author_email='quickstartup@osantana.me',
    url='https://github.com/osantana/quickstartup',
    packages=[
        'quickstartup',
    ],
    include_package_data=True,
    install_requires=[
        "django>=1.9,<1.10",
        "django-widget-tweaks>=1.4,<1.5",
        "django-model-utils>=2.4,<2.6",
        "django-ipware>=1.1.1,<1.2",
        "djmail>=0.12,<0.13",
    ],
    license="MIT",
    zip_safe=False,
    keywords='quickstartup',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={'version': VersionCommand},
)
