# coding: utf-8


from django.conf.urls import url, include
from django.views.generic import TemplateView

from registration.backends.default.views import RegistrationView

from .forms import AuthenticationForm
from .views import UserProfile, UserSecurityProfile, SignupActivationView, UserSocialProfile


urlpatterns = [
    # Auth
    url(r"^signin/$", "quickstartup.accounts.views.login",
        {"template_name": "accounts/signin.html", "authentication_form": AuthenticationForm},
        name="signin"),
    url(r"^signout/$", "django.contrib.auth.views.logout",
        {"next_page": "/"},
        name="signout"),

    # Password reset
    url(r"^password/reset/$", "quickstartup.accounts.views.password_reset", name="password_reset"),
    url(r"^password/reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        "quickstartup.accounts.views.password_reset_confirm",
        name="password_reset_confirm"),

    # Password change
    url(r"^password/change/$", "django.contrib.auth.views.password_change", name="password_change"),
    url(r"^password/change/done/$", "django.contrib.auth.views.password_change_done", name="password_change_done"),

    # Basic Registration
    url(r"^signup/$",
        view=RegistrationView.as_view(
            template_name="accounts/signup.html",
            success_url="qs_accounts:signup_complete",
            disallowed_url="qs_accounts:signup_closed",
        ),
        name="signup"),
    url(r'^signup/complete/$',
        view=TemplateView.as_view(
            template_name='accounts/signup-complete.html',
        ),
        name='signup_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        view=SignupActivationView.as_view(
            template_name='accounts/activation-error.html'
        ),
        name='activate'),
    url(r'^signup/closed/$',
        TemplateView.as_view(template_name='accounts/signup-closed.html'),
        name='signup_closed'),

    # Profile
    url(r"^profile/$", view=UserProfile.as_view(), name="profile"),
    url(r"^profile/security/$", view=UserSecurityProfile.as_view(), name="profile-security"),

    # Social
    url(r"^profile/social/$", view=UserSocialProfile.as_view(), name='profile-social'),
    url("^social-auth-errors/$", "quickstartup.accounts.views.social_auth_errors",
        name='social-auth-errors'),
    url(r"^", include('social.apps.django_app.urls', namespace='social')),
]
