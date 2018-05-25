from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import forms
from . import views

app_name = "qs_accounts"

urlpatterns = [
    # Auth
    path("signin/", views.login,
         {"template_name": "accounts/signin.html", "authentication_form": forms.AuthenticationForm},
         name="signin"),
    path("signout/", auth_views.logout,
         {"next_page": "/"},
         name="signout"),

    # Password reset
    path("password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/<reset_token>/", views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    # Basic Registration
    path("signup/", view=views.SignupView.as_view(), name="signup"),
    path('signup/complete/', view=TemplateView.as_view(template_name='accounts/signup-complete.html', ),
         name='signup_complete'),
    path('activate/<activation_key>/', view=views.SignupActivationView.as_view(), name='activate'),
    path('signup/closed/', TemplateView.as_view(template_name='accounts/signup-closed.html'),
         name='signup_closed'),

    # Profile
    path("profile/", view=views.UserProfileView.as_view(), name="profile"),
    path("profile/password/", views.PasswordChangeView.as_view(), name="password_change"),
    path("profile/email/", views.EmailChangeView.as_view(), name="email_change"),
    path("profile/email/<activation_key>/", views.EmailChangeConfirmationView.as_view(),
         name="email_change_confirmation"),
]
