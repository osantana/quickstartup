# coding: utf-8


from django.db import models, migrations

from quickstartup.website.bootstrap import bootstrap_website_pages


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('slug', models.SlugField(help_text='URL Path. Example: about for /about/', max_length=255, unique=True, blank=True)),
                ('template_name', models.CharField(help_text='Template filename. Example: website/about.html', max_length=255)),
                ('login_required', models.BooleanField(default=False)),
            ],
        ),
        migrations.RunPython(bootstrap_website_pages)
    ]
