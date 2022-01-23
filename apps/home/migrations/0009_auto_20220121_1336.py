# Generated by Django 3.2.6 on 2022-01-21 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20220121_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='activities',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fils', to='home.activity'),
        ),
        migrations.AlterField(
            model_name='student',
            name='allergic',
            field=models.TextField(blank=True, null=True, verbose_name='Allergie à signaler'),
        ),
        migrations.AlterField(
            model_name='student',
            name='chronical_sickness',
            field=models.TextField(blank=True, null=True, verbose_name='maldie chronique à signaler'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_school_attended',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='dernière école fréquentée'),
        ),
        migrations.AlterField(
            model_name='student',
            name='particular_handicap',
            field=models.TextField(blank=True, null=True, verbose_name='handicape particulier à signaler'),
        ),
    ]
