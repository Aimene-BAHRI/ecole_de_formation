# Generated by Django 3.2.6 on 2022-01-21 19:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20220121_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='date_de_creation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]