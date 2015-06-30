# coding: utf-8


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, resolve_url, render
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.module_loading import import_string
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin
from registration.backends.default.views import ActivationView

from .forms import CustomPasswordResetForm, SetPasswordForm
from .utils import get_social_message_errors


PROFILE_FORM_PATH = getattr(settings, "PROFILE_FORM", "quickstartup.accounts.forms.ProfileForm")
PASSWORD_CHANGE_FORM_PATH = getattr(settings, "PASSWORD_CHANGE_FORM", "django.contrib.auth.forms.PasswordChangeForm")
PASSWORD_FORM_PATH = getattr(settings, "PASSWORD_FORM", "quickstartup.accounts.forms.SetPasswordForm")

PROFILE_FORM = import_string(PROFILE_FORM_PATH)
PASSWORD_CHANGE_FORM = import_string(PASSWORD_CHANGE_FORM_PATH)
PASSWORD_FORM = import_string(PASSWORD_FORM_PATH)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    return auth_login(request, *args, **kwargs)


@csrf_protect
def password_reset(request, template_name="accounts/reset.html", mail_template_name="password-reset",
                   password_reset_form=CustomPasswordResetForm,
                   post_reset_redirect=None, extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse("qs_accounts:signin")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)

    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            form.save(request, mail_template_name)
            messages.success(request, _("We've emailed you instructions for setting a new password to the "
                                        "email address you've submitted."))
            return redirect(post_reset_redirect)
    else:
        form = password_reset_form()

    context = {'form': form}
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name="accounts/reset-confirm.html",
                           set_password_form=SetPasswordForm,
                           token_generator=default_token_generator,
                           post_reset_redirect=None, extra_context=None):

    assert uidb64 is not None and token is not None

    if post_reset_redirect is None:
        post_reset_redirect = reverse("qs_accounts:signin")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)

    usermodel = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = usermodel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, usermodel.DoesNotExist):
        messages.error(request, _("Unknown user or invalid token."))
        return redirect(post_reset_redirect)

    if not token_generator.check_token(user, token):
        messages.error(request, _("Unknown user or invalid token."))
        return redirect(post_reset_redirect)

    if request.method == 'POST':
        form = set_password_form(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Password has been reset successfully."))
            return redirect(post_reset_redirect)
    else:
        form = set_password_form(user)

    context = {'form': form}
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context)


# noinspection PyUnresolvedReferences
class ProfileMixin(object):
    def get_object(self, *args, **kwargs):
        return self.request.user


class UserProfile(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile')
    form_class = PROFILE_FORM
    template_name = 'accounts/profile.html'

    def form_valid(self, form):
        messages.success(self.request, _(u'Succesfully updated profile.'))
        return super(UserProfile, self).form_valid(form)


class UserSecurityProfile(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile-security')
    form_class = PASSWORD_CHANGE_FORM
    form_class_without_password = PASSWORD_FORM
    template_name = 'accounts/profile-security.html'

    def get_form_class(self):
        # Probably, user was authenticated with social auth
        if not self.request.user.has_usable_password():
            return self.form_class_without_password or self.form_class
        return self.form_class

    def form_valid(self, form):
        messages.success(self.request, _(u'Succesfully updated your password.'))
        return super(UserSecurityProfile, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserSecurityProfile, self).get_form_kwargs()
        kwargs.update({'user': self.object})
        if 'instance' in kwargs:
            del kwargs['instance']
        return kwargs


class SignupActivationView(ActivationView):
    def activate(self, request, activation_key):
        activated_user = super().activate(request, activation_key)

        if activated_user:
            site = get_current_site(request)
            messages.success(request, _("Welcome to {}! Your account was successfully activated.".format(site.name)))

        return activated_user

    def get_success_url(self, request, user):
        return settings.LOGIN_REDIRECT_URL, (), {}


class UserSocialProfile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile-social.html'

    def get_context_data(self, **kwargs):
        context = super(UserSocialProfile, self).get_context_data(**kwargs)
        context['error_messages'] = get_social_message_errors(self.request)
        return context


@never_cache
def social_auth_errors(request, default_redirect='qs_accounts:signup'):
    """Handles social auth errors. Some assumptions here is:
        - If the user is authenticated, then he will be redirected to social profile view
        - If the user is not authenticated, then he will be redirect to the <default_redirect> view,
          defaults to sign-up view
    """
    if request.user.is_authenticated():
        url = reverse('qs_accounts:profile-social')
    else:
        url = reverse(default_redirect)

    args = request.META.get('QUERY_STRING', '')
    if args:
        url = '{}?{}'.format(url, args)

    return redirect(url)
