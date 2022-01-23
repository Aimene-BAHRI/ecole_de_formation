# Generated by Django 3.2.6 on 2022-01-22 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20220122_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='subscribed_plan',
            field=models.CharField(choices=[('mentuelle', 'Mentuelle'), ('trimestrielle', 'Trimestrielle'), ('6_mois', '6 Mois'), ('annuelle', 'Annuelle')], default='mentuelle', max_length=30, verbose_name="le plan d'abonement"),
        ),
    ]