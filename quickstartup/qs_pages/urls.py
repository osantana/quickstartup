from django.urls import path

from . import views

app_name = "qs_pages"

urlpatterns = [
    path("", views.index, name="index"),
]
