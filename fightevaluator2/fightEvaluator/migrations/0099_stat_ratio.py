# Generated by Django 5.1.2 on 2025-02-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0098_remove_matchup_scheduled'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='ratio',
            field=models.FloatField(default=0.0),
        ),
    ]
