# Generated by Django 5.0 on 2023-12-18 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0002_alter_fighter_nick_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fighter',
            old_name='api_link',
            new_name='data_api_link',
        ),
    ]
