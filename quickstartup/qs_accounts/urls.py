# coding: utf-8


from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import forms
from . import views

urlpatterns = [
    # Auth
    url(r"^signin/$", views.login,
        {"template_name": "accounts/signin.html", "authentication_form": forms.AuthenticationForm},
        name="signin"),
    url(r"^signout/$", auth_views.logout,
        {"next_page": "/"},
        name="signout"),

    # Password reset
    url(r"^password/reset/$", views.password_reset, name="password_reset"),
    url(r"^password/reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.password_reset_confirm,
        name="password_reset_confirm"),

    # Password change
    url(r"^password/change/$", auth_views.password_change, name="password_change"),
    url(r"^password/change/done/$", auth_views.password_change_done, name="password_change_done"),

    # Basic Registration
    url(r"^signup/$",
        view=views.SignupView.as_view(
                template_name="accounts/signup.html",
                success_url="qs_accounts:signup_complete",
                # disallowed_url="qs_accounts:signup_closed",
        ),
        name="signup"),

    url(r'^signup/complete/$',
        view=TemplateView.as_view(
                template_name='accounts/signup-complete.html',
        ),
        name='signup_complete'),
    # url(r'^activate/(?P<activation_key>\w+)/$',
    #     view=SignupActivationView.as_view(
    #             template_name='accounts/activation-error.html'
    #     ),
    #     name='activate'),
    url(r'^signup/closed/$',
        TemplateView.as_view(template_name='accounts/signup-closed.html'),
        name='signup_closed'),

    # Profile
    url(r"^profile/$", view=views.UserProfile.as_view(), name="profile"),
    url(r"^profile/security/$", view=views.UserSecurityProfile.as_view(), name="profile-security"),
]
