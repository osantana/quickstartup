# coding: utf-8


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.ContactView.as_view(), name="contact"),
]
