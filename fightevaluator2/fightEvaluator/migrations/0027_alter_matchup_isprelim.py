# Generated by Django 5.0 on 2023-12-21 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0026_matchup_isprelim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchup',
            name='isprelim',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
