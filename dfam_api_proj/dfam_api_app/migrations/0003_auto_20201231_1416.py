# Generated by Django 3.1.4 on 2020-12-31 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dfam_api_app', '0002_auto_20201231_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafilesub',
            name='data_file_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_file_type_sub', to='dfam_api_app.datafiletype'),
        ),
    ]
