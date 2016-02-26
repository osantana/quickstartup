# coding: utf-8


from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, "apps/index.html")


urlpatterns = [
    url(r"^", index, name="index"),
]
