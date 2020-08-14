from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('qs_contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='contact ip'),
        ),
    ]
