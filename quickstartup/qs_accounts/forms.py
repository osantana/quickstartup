# coding: utf-8


from django import forms
from django.contrib.auth import forms as django_forms, get_user_model
from django.contrib.auth import password_validation
from django.core.signing import TimestampSigner, Signer
from django.utils.translation import ugettext_lazy as _
from djmail import template_mail

from quickstartup.qs_core.antispam import AntiSpamField
from quickstartup.qs_core.widgets import EmailInput
from quickstartup.settings_utils import get_configuration
from .signals import user_registered


UserModel = get_user_model()


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password (verify)'), widget=forms.PasswordInput)
    antispam = AntiSpamField()

    class Meta:
        model = UserModel
        fields = ('name', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password_validation.validate_password(password1, self.instance)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")

        return password2

    def send_activation_email(self, request, user):
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

    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()

        self.send_activation_email(request, user)
        user_registered.send(sender=self.__class__, user=user, request=request)
        return user


class AuthenticationForm(django_forms.AuthenticationForm):
    username = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput())

    def get_users(self):
        email = self.cleaned_data["email"]
        return UserModel.objects.filter(email__iexact=email, is_active=True)

    def send_password_reset_email(self, request, user):
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

    def save(self, request):
        for user in self.get_users():
            self.send_password_reset_email(request, user)


class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput())
    new_password2 = forms.CharField(label=_("New password (verify)"), widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password1(self):
        password1 = self.cleaned_data['new_password1']
        password_validation.validate_password(password1, self.user)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.", code='password_mismatch')
        return password2

    # noinspection PyUnusedLocal
    def save(self, request):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ("name", "email")


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label=_("Current"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("New"), widget=forms.PasswordInput,
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirmation"), widget=forms.PasswordInput)

    def __init__(self, instance, *args, **kwargs):
        self.user = instance
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Your old password was entered incorrectly. Please enter it again."),
                                        code='password_incorrect')
        return old_password

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")
        password_validation.validate_password(password1, self.user)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."), code='password_mismatch')
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class EmailChangeForm(forms.ModelForm):
    new_email = forms.EmailField(label=_("New E-Mail"), widget=forms.EmailInput)

    class Meta:
        model = UserModel
        fields = ('new_email',)

    def send_change_email(self, request, user):
        signer = Signer()
        context = {
            'request': request,
            'user': user,
            'activation_key': signer.sign(user.get_username()),
            'project_name': get_configuration("QS_PROJECT_NAME"),
            'project_url': get_configuration("QS_PROJECT_URL"),
        }
        mails = template_mail.MagicMailBuilder()
        email = mails.change_email(user.new_email, context)
        email.send()

    def save(self, commit=True, request=None):
        user = super().save(commit=commit)
        self.send_change_email(request, user)
        return self.instance
