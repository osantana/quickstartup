# coding: utf-8


from django.conf.urls import include, url
from django.contrib import admin

from .settings_utils import get_configuration

admin.autodiscover()

urlpatterns = []

if get_configuration("QS_ADMIN_URL"):
    urlpatterns += [
        url(r"^{}/".format(get_configuration("QS_ADMIN_URL").rstrip("/")), include(admin.site.urls)),
    ]

urlpatterns += [
    url(r"^accounts/", include("quickstartup.qs_accounts.urls", namespace="qs_accounts")),
    url(r"^contact/", include("quickstartup.qs_contacts.urls", namespace="qs_contacts")),
    url(r"^", include("quickstartup.qs_website.urls", namespace="qs_pages")),
]
