# coding: utf-8


from django.conf.urls import url
from django.http.response import HttpResponse


def index(request):
    return HttpResponse("OK")


urlpatterns = [
    url(r"^", index, name="index"),
]
