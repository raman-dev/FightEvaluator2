# Generated by Django 5.1.2 on 2025-02-21 16:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0108_alter_pick_prediction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pick',
            name='prediction',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fightEvaluator.prediction2'),
        ),
    ]
