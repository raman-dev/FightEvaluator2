# Generated by Django 5.1.2 on 2025-02-20 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0107_pick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pick',
            name='prediction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fightEvaluator.prediction2'),
        ),
    ]
