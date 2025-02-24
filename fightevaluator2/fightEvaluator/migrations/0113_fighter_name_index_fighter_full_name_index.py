# Generated by Django 5.1.2 on 2025-02-24 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0112_remove_fighter_name_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='name_index',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddIndex(
            model_name='fighter',
            index=models.Index(fields=['name_index'], name='full_name_index'),
        ),
    ]
