# coding: utf-8


from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import (AbstractBaseUser as DjangoAbstractBaseUser,
                                           BaseUserManager as DjangoBaseUserManager)

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseUserManager(DjangoBaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        email = self.normalize_email(email)

        user_model = get_user_model()
        user = user_model(email=email, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, is_staff=False, **extra_fields):
        return self._create_user(email, password, is_staff, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def activate(self, username):
        user = self.get_by_natural_key(username)
        user.is_active = True
        user.save()
        return user

    def confirm_new_email(self, username):
        user = self.get_by_natural_key(username)
        user.confirm_new_email()
        return user


# noinspection PyAbstractClass
class AbstractBaseUser(DjangoAbstractBaseUser):
    objects = BaseUserManager()

    email = models.EmailField(_("e-mail"), max_length=255, unique=True, db_index=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)

    new_email = models.EmailField(_("new e-mail"), max_length=255, null=True, blank=True, db_index=True)

    USERNAME_FIELD = "email"

    class Meta(DjangoAbstractBaseUser.Meta):
        abstract = True

    def get_short_name(self):
        return self.email

    def confirm_new_email(self):
        if not self.new_email:
            return

        self.email = self.new_email
        self.new_email = None
        self.save()


class AbstractUser(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta(AbstractBaseUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        return self.name


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
