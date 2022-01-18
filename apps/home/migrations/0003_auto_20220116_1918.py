# Generated by Django 3.2.6 on 2022-01-16 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220110_0149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fils',
            name='matiere',
        ),
        migrations.AlterField(
            model_name='cours_particulier',
            name='categorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etudiants', to='home.categorie', verbose_name='categorie'),
        ),
        migrations.AlterField(
            model_name='fils',
            name='gender',
            field=models.CharField(choices=[('homme', 'Homme'), ('femme', 'Femme')], default='homme', max_length=10),
        ),
    ]