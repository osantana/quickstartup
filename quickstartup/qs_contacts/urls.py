from django.urls import path

from . import views

app_name = "qs_contacts"

urlpatterns = [
    path("", views.ContactView.as_view(), name="contact"),
]
