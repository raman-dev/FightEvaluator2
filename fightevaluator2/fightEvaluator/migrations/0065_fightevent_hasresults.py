# Generated by Django 5.0.4 on 2024-05-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0064_alter_matchup_outcome'),
    ]

    operations = [
        migrations.AddField(
            model_name='fightevent',
            name='hasResults',
            field=models.BooleanField(default=False),
        ),
    ]
