# Generated by Django 5.0 on 2024-01-22 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0039_matchupoutcome_justification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prediction', models.CharField(choices=[('Win', 'Fighter wins'), ('1.5 >= Rnds', 'Fight lasts more than 1.5 rounds'), ('No', 'Fight Does Not Go the Distance')], max_length=256)),
                ('result', models.CharField(blank=True, choices=[('Win', 'Fighter wins'), ('1.5 >= Rnds', 'Fight lasts more than 1.5 rounds'), ('No', 'Fight Does Not Go the Distance')], default=None, max_length=256, null=True)),
                ('matchup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fightEvaluator.matchup')),
            ],
        ),
    ]