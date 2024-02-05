# Generated by Django 5.0 on 2024-02-05 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0052_remove_matchup_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlikelihood',
            name='likelihood',
            field=models.IntegerField(blank=True, choices=[(5, 'Very Unlikely'), (4, 'Somewhat Unlikely'), (3, 'Neutral'), (2, 'Likely'), (1, 'Very Likely'), (0, 'Not Predicted')], default=0, null=True),
        ),
    ]
