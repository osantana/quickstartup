# coding: utf-8

from django.dispatch import Signal

user_registered = Signal(providing_args=["user", "request"])
user_activated = Signal(providing_args=["user", "request"])
