# coding: utf-8


from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = []

if settings.ADMIN_URL:
    urlpatterns += [
        url(r"^{}/".format(settings.ADMIN_URL), include(admin.site.urls)),
    ]

urlpatterns += [
    url(r"^accounts/", include("quickstartup.qs_accounts.urls", namespace="qs_accounts")),
    url(r"^contact/", include("quickstartup.qs_contacts.urls", namespace="qs_contacts")),
    url(r"^", include("quickstartup.qs_website.urls", namespace="qs_pages")),
]
