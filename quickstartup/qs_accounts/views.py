# coding: utf-8


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as user_login, get_user_model, get_backends
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login as auth_login
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature, Signer
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import UpdateView, FormView, TemplateView, RedirectView

from quickstartup.settings_utils import get_configuration, get_object_from_configuration
from .signals import user_activated

SECONDS_IN_DAY = 24 * 60 * 60


# noinspection PyUnresolvedReferences
class ProfileMixin(object):
    # noinspection PyUnusedLocal
    def get_object(self, *args, **kwargs):
        return self.request.user


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    return auth_login(request, *args, **kwargs)


class PasswordResetView(FormView):
    template_name = "accounts/reset.html"
    success_url = reverse_lazy("qs_accounts:signin")

    def get_form_class(self):
        return get_object_from_configuration("QS_PASSWORD_RESET_FORM")

    def form_valid(self, form):
        form.save(self.request)
        messages.success(self.request, _("We've e-mailed you instructions for setting a new password to the "
                                         "e-mail address you've submitted."))
        return super().form_valid(form)


class PasswordResetConfirmView(FormView):
    template_name = "accounts/reset-confirm.html"
    success_url = reverse_lazy("qs_accounts:signin")

    # noinspection PyMethodOverriding
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, reset_token, *args, **kwargs):
        try:
            self.get_username()
        except SignatureExpired:
            messages.error(request, _("Password reset token expired."))
            return redirect(self.get_success_url())
        except BadSignature:
            messages.error(request, _("Invalid password reset token."))
            return redirect(self.get_success_url())
        return super().dispatch(request, reset_token, *args, **kwargs)

    def get_username(self):
        reset_token = self.kwargs["reset_token"]
        signer = TimestampSigner()
        expiration = get_configuration("PASSWORD_RESET_TIMEOUT_DAYS")
        return signer.unsign(reset_token, max_age=expiration * SECONDS_IN_DAY)

    def get_user(self):
        user_model = get_user_model()

        try:
            user = user_model.objects.get_by_natural_key(self.get_username())
        except user_model.DoesNotExist:
            return

        return user

    def get_form_class(self):
        return get_object_from_configuration("QS_PASSWORD_RESET_CONFIRM_FORM")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if 'user' in kwargs:
            return kwargs

        kwargs['user'] = self.get_user()
        return kwargs

    def form_valid(self, form):
        form.save(self.request)
        messages.success(self.request, _("Password has been reset successfully."))
        return super().form_valid(form)


class SignupView(FormView):
    template_name = "accounts/signup.html"
    disallowed_url = reverse_lazy("qs_accounts:signup_closed")
    success_url = reverse_lazy("qs_accounts:signup_complete")

    def dispatch(self, request, *args, **kwargs):
        allowed = get_configuration("QS_SIGNUP_OPEN")
        if not allowed:
            return redirect(self.disallowed_url)
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_object_from_configuration("QS_SIGNUP_FORM")

    def form_valid(self, form):
        form.save(request=self.request)
        messages.success(self.request, _("We've e-mailed you instructions for setting a new password to the "
                                         "e-mail address you've submitted."))

        return super().form_valid(form)


class SignupActivationView(TemplateView):
    template_name = 'accounts/activation-error.html'

    def get_success_url(self):
        return get_configuration("LOGIN_REDIRECT_URL")

    # noinspection PyMethodOverriding
    def get(self, request, activation_key, *args, **kwargs):
        signer = TimestampSigner()
        expiration = get_configuration("QS_SIGNUP_TOKEN_EXPIRATION_DAYS")
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

        if get_configuration("QS_SIGNUP_AUTO_LOGIN"):
            self._login_user(request, user)
        return redirect(self.get_success_url())

    def _login_user(self, request, user):
        backend = get_backends()[0]  # Hack to bypass `authenticate()`.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        user_login(request, user)
        request.session['QS_SIGNUP_AUTO_LOGIN'] = True
        request.session.modified = True


class UserProfileView(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile')
    form_class = import_string(get_configuration("QS_PROFILE_FORM"))
    template_name = 'accounts/profile.html'

    def form_valid(self, form):
        messages.success(self.request, _(u'Succesfully updated profile.'))
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile')
    form_class = get_object_from_configuration("QS_PASSWORD_CHANGE_FORM")
    template_name = 'accounts/password-change.html'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _(u'Succesfully updated your password.'))
        return super().form_valid(form)


class EmailChangeView(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile')
    form_class = get_object_from_configuration("QS_EMAIL_CHANGE_FORM")
    template_name = 'accounts/email-change.html'

    def form_valid(self, form):
        messages.success(self.request, _(u"You'll receive an message in your new e-mail to check it."))
        return super().form_valid(form)


class EmailChangeConfirmationView(LoginRequiredMixin, ProfileMixin, RedirectView):
    url = reverse_lazy("qs_accounts:profile")

    # noinspection PyMethodOverriding
    def get(self, request, activation_key, *args, **kwargs):
        signer = Signer()
        try:
            username = signer.unsign(activation_key)
        except BadSignature:
            messages.error(self.request, _(u"Invalid e-mail configuration token."))
            return super().get(request, *args, **kwargs)

        user_model = get_user_model()
        try:
            user_model.objects.confirm_new_email(username)
            messages.success(self.request, _(u"New e-mail has been successfully configured."))
        except user_model.DoesNotExist:
            messages.error(self.request, _(u"E-mail not found."))

        return super().get(request, *args, **kwargs)
