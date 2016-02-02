# coding: utf-8


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, get_backends
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login as auth_login
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, resolve_url, render
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import UpdateView, FormView, TemplateView

from quickstartup.settings_utils import get_settings, get_object_from_settings
from .forms import CustomPasswordResetForm, SetPasswordForm
from .signals import user_activated

SECONDS_IN_DAY = 24 * 60 * 60


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    return auth_login(request, *args, **kwargs)


@csrf_protect
def password_reset(request, template_name="qs_accounts/reset.html",
                   password_reset_form=CustomPasswordResetForm,
                   post_reset_redirect=None, extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse("qs_accounts:signin")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)

    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            form.save(request)
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
def password_reset_confirm(request, reset_token,
                           template_name="accounts/reset-confirm.html",
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None):

    if post_reset_redirect is None:
        post_reset_redirect = reverse("qs_accounts:signin")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)

    signer = TimestampSigner()
    expiration = get_settings("PASSWORD_RESET_TIMEOUT_DAYS")
    try:
        username = signer.unsign(reset_token, max_age=expiration * SECONDS_IN_DAY)
    except (BadSignature, SignatureExpired):
        messages.error(request, _("Invalid token."))
        return redirect(post_reset_redirect)

    user_model = get_user_model()
    try:
        user = user_model.objects.activate(username)
    except user_model.DoesNotExist:
        messages.error(request, _("User not found."))
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
    return render(request, template_name, context)


# noinspection PyUnresolvedReferences
class ProfileMixin(object):
    # noinspection PyUnusedLocal
    def get_object(self, *args, **kwargs):
        return self.request.user


class UserProfile(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile')
    form_class = import_string(get_settings("QS_PROFILE_FORM"))
    template_name = 'accounts/profile.html'

    def form_valid(self, form):
        messages.success(self.request, _(u'Succesfully updated profile.'))
        return super(UserProfile, self).form_valid(form)


class UserSecurityProfile(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile-security')
    form_class = get_object_from_settings("QS_PASSWORD_CHANGE_FORM")
    form_class_without_password = get_object_from_settings("QS_PASSWORD_FORM")
    template_name = 'accounts/profile-security.html'

    def get_form_class(self):
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


class SignupView(FormView):
    template_name = "accounts/signup.html"
    disallowed_url = reverse_lazy("qs_accounts:signup_closed")
    success_url = reverse_lazy("qs_accounts:signup_complete")

    def dispatch(self, request, *args, **kwargs):
        allowed = get_settings("QS_SIGNUP_OPEN")
        if not allowed:
            return redirect(self.disallowed_url)
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_object_from_settings("QS_SIGNUP_FORM")

    def form_valid(self, form):
        form.finish(self.request)
        return super().form_valid(form)


class SignupActivationView(TemplateView):
    template_name = 'accounts/activation-error.html'

    def get_success_url(self):
        return get_settings("LOGIN_REDIRECT_URL")

    def get(self, request, activation_key, *args, **kwargs):
        signer = TimestampSigner()
        expiration = get_settings("QS_SIGNUP_TOKEN_EXPIRATION_DAYS")
        try:
            username = signer.unsign(activation_key, max_age=expiration * SECONDS_IN_DAY)
        except (BadSignature, SignatureExpired):
            return super().get(request, *args, **kwargs)

        user_model = get_user_model()
        try:
            user = user_model.objects.activate(username)
        except user_model.DoesNotExist:
            return super().get(request, *args, **kwargs)

        if user.is_active:
            user_activated.send(sender=self.__class__, user=user, request=request)

        if get_settings("QS_SIGNUP_AUTO_LOGIN"):
            self._login_user(request, user)
        return redirect(self.get_success_url())

    def _login_user(self, request, user):
        backend = get_backends()[0]  # Hack to bypass `authenticate()`.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(request, user)
        request.session['QS_SIGNUP_AUTO_LOGIN'] = True
        request.session.modified = True
