# Generated by Django 3.2.6 on 2022-02-08 06:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20220206_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours_particulier',
            name='date_de_creation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
