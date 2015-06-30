# coding: utf-8


from django.conf.urls import url
from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "apps/index.html")


urlpatterns = [
    url(r"^", index, name="index"),
]
