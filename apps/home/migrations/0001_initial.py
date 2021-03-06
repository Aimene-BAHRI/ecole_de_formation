# Generated by Django 3.2.6 on 2022-01-08 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_operation', models.CharField(choices=[('entrée', 'entrée'), ('sortie', 'sortie')], default='sortie', max_length=20)),
                ('somme_operation', models.DecimalField(decimal_places=2, max_digits=100)),
                ('description', models.CharField(max_length=200)),
                ('date_de_creation', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('closed', 'Closed')], default='active', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Magazin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_magazin', models.CharField(max_length=300)),
                ('caisse', models.DecimalField(decimal_places=2, default=0, max_digits=100)),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_matiere', models.CharField(default='', max_length=300)),
                ('prix_matiere', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.IntegerField()),
                ('date_paid', models.DateField(default=django.utils.timezone.now)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.facture')),
            ],
        ),
        migrations.CreateModel(
            name='Parant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_parent', models.CharField(max_length=100, verbose_name='nom du parant')),
                ('prenom_parent', models.CharField(max_length=100, verbose_name='nom du parant')),
                ('telephone', models.CharField(max_length=20, verbose_name='numero de telephone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parant', to=settings.AUTH_USER_MODEL, verbose_name='utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.facture')),
            ],
        ),
        migrations.CreateModel(
            name='Fils',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom_fils', models.CharField(max_length=200, verbose_name='nom fils')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('niveau_etude', models.CharField(choices=[('prescolaire', 'Prescolaire'), ('preparatoire', 'Preparatoire'), ('primaire', 'Primaire'), ('moyenne', 'Moyenne'), ('lycéenne', 'Lycéenne')], default='prescolaire', max_length=200, verbose_name="niveau d'etude")),
                ('matiere', models.ManyToManyField(related_name='etudiants', to='home.Matiere', verbose_name='matiere')),
                ('parant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fils', to='home.parant')),
            ],
        ),
        migrations.AddField(
            model_name='facture',
            name='magazin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factures_magazin', to='home.magazin'),
        ),
        migrations.AddField(
            model_name='facture',
            name='operateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factures', to=settings.AUTH_USER_MODEL),
        ),
    ]
