from django.urls import path

from .views import index


app_name = "app"


urlpatterns = [
    path("", index, name="index"),
]
