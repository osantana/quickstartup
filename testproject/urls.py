# coding: utf-8


from django.conf.urls import include, url


urlpatterns = [
    url(r"^app/", include("testproject.testapp", namespace="app")),
    url(r"^", include("quickstartup.urls")),
]
