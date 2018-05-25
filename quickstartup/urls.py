from django.contrib import admin
from django.urls import include, path

from .settings_utils import get_configuration

admin.autodiscover()

urlpatterns = []

if get_configuration("QS_ADMIN_URL"):
    urlpatterns += [
        path("{}/".format(get_configuration("QS_ADMIN_URL").rstrip("/")), admin.site.urls),
    ]

urlpatterns += [
    path("accounts/", include("quickstartup.qs_accounts.urls", namespace="qs_accounts")),
    path("contact/", include("quickstartup.qs_contacts.urls", namespace="qs_contacts")),
    path("", include("quickstartup.qs_pages.urls", namespace="qs_pages")),
]
