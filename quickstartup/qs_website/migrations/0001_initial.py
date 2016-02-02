# coding: utf-8


from django.db import migrations, models

from quickstartup.qs_website.bootstrap import bootstrap_website_pages


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
                name='Page',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('slug', models.SlugField(blank=True, help_text='URL Path. Example: about for /about/', max_length=255, unique=True)),
                    ('template_name', models.CharField(help_text='Template filename. Example: website/about.html', max_length=255)),
                    ('login_required', models.BooleanField(default=False)),
                ],
        ),
        migrations.RunPython(bootstrap_website_pages),
    ]
