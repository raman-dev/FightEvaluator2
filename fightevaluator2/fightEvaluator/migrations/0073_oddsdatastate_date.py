# Generated by Django 5.1.2 on 2024-11-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0072_oddsdatastate_alter_matchup_fighter_a_references_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='oddsdatastate',
            name='date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
