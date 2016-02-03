# coding: utf-8


from django import forms
from django.contrib.auth import forms as django_forms
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
from django.utils.translation import ugettext_lazy as _
from djmail import template_mail

from quickstartup.settings_utils import get_configuration
from .models import User
from .signals import user_registered
from ..widgets import EmailInput


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password (verify)'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def _send_activation_email(self, request, user):
        signer = TimestampSigner()
        context = {
            'request': request,
            'user': user,
            'activation_key': signer.sign(user.get_username()),
            'project_name': get_configuration("QS_PROJECT_NAME"),
            'project_url': get_configuration("QS_PROJECT_URL"),
            'expiration_days': get_configuration("QS_SIGNUP_TOKEN_EXPIRATION_DAYS"),
        }
        mails = template_mail.MagicMailBuilder()
        email = mails.activation(user, context)
        email.send()

    def finish(self, request):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()

        self._send_activation_email(request, user)
        user_registered.send(sender=self.__class__, user=user, request=request)


class AuthenticationForm(django_forms.AuthenticationForm):
    username = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput())

    def save(self, request):
        email = self.cleaned_data["email"]

        user_model = get_user_model()
        active_users = user_model.objects.filter(email__iexact=email, is_active=True)

        for user in active_users:
            signer = TimestampSigner()
            reset_token = signer.sign(user.get_username())
            context = {
                "request": request,
                "user": user,
                "project_name": get_configuration("QS_PROJECT_NAME"),
                "project_url": get_configuration("QS_PROJECT_URL"),
                "reset_token": reset_token,
            }

            mails = template_mail.MagicMailBuilder()
            email = mails.password_reset(user, context)
            email.send()


class SetPasswordForm(django_forms.SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput())
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email")
