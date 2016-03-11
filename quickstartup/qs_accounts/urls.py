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
    url(r"^password/reset/$", views.PasswordResetView.as_view(), name="password_reset"),
    url(r"^password/reset/(?P<reset_token>.+)/$", views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"),

    # Basic Registration
    url(r"^signup/$", view=views.SignupView.as_view(), name="signup"),
    url(r'^signup/complete/$', view=TemplateView.as_view(template_name='accounts/signup-complete.html', ),
        name='signup_complete'),
    url(r'^activate/(?P<activation_key>[^/]+)/$', view=views.SignupActivationView.as_view(), name='activate'),
    url(r'^signup/closed/$', TemplateView.as_view(template_name='accounts/signup-closed.html'),
        name='signup_closed'),

    # Profile
    url(r"^profile/$", view=views.UserProfileView.as_view(), name="profile"),
    url(r"^profile/password/$", views.PasswordChangeView.as_view(), name="password_change"),
    url(r"^profile/email/$", views.EmailChangeView.as_view(), name="email_change"),
    url(r"^profile/email/(?P<activation_key>[^/]+)/$", views.EmailChangeConfirmationView.as_view(),
        name="email_change_confirmation"),
]
