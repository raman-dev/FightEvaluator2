# Generated by Django 5.1.2 on 2025-01-01 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0083_matchup2'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup2',
            name='analysis_complete',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
