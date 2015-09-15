# coding: utf-8

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1', verbose_name='contact ip'),
            preserve_default=False,
        ),
    ]
