# Generated by Django 5.0 on 2024-02-07 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0055_rename_event_name_eventlikelihood_event_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventlikelihood',
            old_name='event_type',
            new_name='eventType',
        ),
    ]
