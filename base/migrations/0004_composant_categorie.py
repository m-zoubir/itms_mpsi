# Generated by Django 5.2.1 on 2025-05-18 03:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_composant_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='composant',
            name='categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.categorie'),
        ),
    ]
