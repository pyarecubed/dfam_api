# Generated by Django 3.1.4 on 2020-12-31 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dfam_api_app', '0003_auto_20201231_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafilesub',
            name='uuid',
            field=models.CharField(max_length=36, unique=True),
        ),
    ]
