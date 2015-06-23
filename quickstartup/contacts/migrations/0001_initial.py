# coding: utf-8


from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(verbose_name='status', default='N', max_length=1, choices=[('N', 'New'), ('O', 'Ongoing'), ('R', 'Resolved'), ('C', 'Closed'), ('I', 'Invalid')])),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('email', models.EmailField(verbose_name='email', max_length=255)),
                ('phone', models.CharField(verbose_name='phone', max_length=100, blank=True)),
                ('message', models.TextField(verbose_name='message')),
            ],
        ),
    ]
