from django.conf import settings
from django.db import models
from django.utils.timezone import now

YEARS_DAY = 365


class TestProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    birthday = models.DateField()

    @property
    def age(self):
        return int((now().replace(tzinfo=None) - self.birthday).days / YEARS_DAY)

    def get_birthdate(self, date_format="%d/%m"):
        return self.birthday.strftime(date_format)
