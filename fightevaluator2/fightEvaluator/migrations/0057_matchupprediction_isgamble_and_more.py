# Generated by Django 5.0 on 2024-02-12 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0056_rename_event_type_eventlikelihood_eventtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchupprediction',
            name='isGamble',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='eventlikelihood',
            name='event',
            field=models.CharField(choices=[('Win', 'Fighter wins'), ('Yes', 'Fight Goes the Distance'), ('No', 'Fight Does Not Go the Distance'), ('Rnds >= 0.5', 'Fight lasts more than 0.5 rounds'), ('Rnds >= 1.5', 'Fight lasts more than 1.5 rounds'), ('Rnds >= 2.5', 'Fight lasts more than 2.5 rounds'), ('Rnds >= 3.5', 'Fight lasts more than 3.5 rounds'), ('Rnds >= 4.5', 'Fight lasts more than 4.5 rounds'), ('NA', 'Not Available')], max_length=256),
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isGamble', models.BooleanField(default=False)),
                ('matchup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fightEvaluator.matchup')),
                ('prediction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fightEvaluator.eventlikelihood')),
            ],
        ),
    ]
