# Generated by Django 5.0 on 2023-12-19 19:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0015_rename_note_note_data_alter_note_createdat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 12, 19, 19, 27, 46, 805523, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
