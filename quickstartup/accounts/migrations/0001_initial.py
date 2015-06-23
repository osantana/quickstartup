# coding: utf-8


from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(max_length=255, verbose_name='email', unique=True, db_index=True)),
                ('date_joined', models.DateTimeField(default=timezone.now, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_query_name='user', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.Permission', help_text='Specific permissions for this user.', verbose_name='user permissions', related_query_name='user', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'swappable': 'AUTH_USER_MODEL',
                'abstract': False,
                'verbose_name': 'user',
            },
        ),
    ]
