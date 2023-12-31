# Generated by Django 5.0 on 2023-12-18 23:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0010_fighter_assessment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_movement', models.IntegerField(choices=[(0, 'Untested')], default=0, max_length=100)),
                ('fighter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fightEvaluator.fighter')),
            ],
        ),
    ]
