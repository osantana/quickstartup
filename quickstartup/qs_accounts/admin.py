# coding: utf-8


from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password (verify)'), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password1', 'password2', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("name", "email", "password", "is_staff", "is_superuser")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ("name", "email", "is_staff", "last_login")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "email", "password1", "password2", "is_staff"),
        },),
    )
    search_fields = ("name", "email")
    ordering = ("name", "email")


# Enable admin interface if User is the quickstart user model
if get_user_model() is User:
    admin.site.register(User, UserAdmin)
