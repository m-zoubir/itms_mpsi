# Generated by Django 5.2.1 on 2025-05-18 01:55

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id_categorie', models.AutoField(primary_key=True, serialize=False)),
                ('designation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_materiel', models.CharField(choices=[('Ordinateur', 'Ordinateur'), ('Imprimante', 'Imprimante'), ('Serveur', 'Serveur'), ('Autre', 'Autre')], max_length=100)),
                ('marque', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_inventaire', models.CharField(max_length=100)),
                ('service_affectation', models.CharField(max_length=100)),
                ('date_depot', models.DateTimeField(auto_now_add=True)),
                ('nom_deposant', models.CharField(max_length=100)),
                ('numero_telephone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=100)),
                ('status', models.CharField(choices=[('Etudiant', 'Etudiant'), ('Enseignant', 'Enseignant'), ('Employe', 'Employe')], max_length=100)),
                ('panne_declaree', models.TextField(blank=True, null=True)),
                ('status_demande', models.CharField(choices=[('Nouvelle', 'Nouvelle'), ('Acceptee', 'Acceptee'), ('Rejetee', 'Rejetée')], default='Nouvelle', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equipement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_reference', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('numero_serie', models.CharField(max_length=100)),
                ('designation', models.TextField()),
                ('observation', models.TextField(blank=True, null=True)),
                ('numero_inventaire', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Composant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_composant', models.CharField(choices=[('Nouveau', 'Nouveau'), ('Ancien', 'Ancien')], max_length=20)),
                ('model_reference', models.TextField(blank=True, null=True)),
                ('numero_serie', models.CharField(max_length=100)),
                ('designation', models.TextField()),
                ('observation', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('numero_serie_eq_source', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_inventaire_eq_source', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('Used', 'Used'), ('Free', 'Free')], max_length=20, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('disponible', models.BooleanField(blank=True, default=True, null=True)),
                ('categorie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('numero_serie', models.CharField(blank=True, max_length=100, null=True)),
                ('priorite', models.CharField(choices=[('Haute', 'Haute'), ('Moyenne', 'Moyenne'), ('Basse', 'Basse')], default='Moyenne', max_length=100)),
                ('panne_trouvee', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('enCours', 'enCours'), ('Termine', 'Termine'), ('Irreparable', 'Irreparable')], default='enCours', max_length=100)),
                ('date_sortie', models.DateTimeField(blank=True, null=True)),
                ('composants_utilises', models.ManyToManyField(blank=True, to='base.composant')),
                ('demande_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interventions', to='base.demande')),
                ('technicien', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interventions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
