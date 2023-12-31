# Generated by Django 5.0 on 2023-12-20 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0024_alter_fighter_data_api_link_alter_fighter_img_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fighter',
            name='date_of_birth',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='matchup',
            name='event',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fightEvaluator.fightevent'),
        ),
        migrations.AlterField(
            model_name='matchup',
            name='rounds',
            field=models.IntegerField(blank=True, default=3, null=True),
        ),
        migrations.AlterField(
            model_name='matchup',
            name='scheduled',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
