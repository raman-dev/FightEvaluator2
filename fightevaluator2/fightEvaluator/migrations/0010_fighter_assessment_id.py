# Generated by Django 5.0 on 2023-12-18 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0009_fighter_img_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='assessment_id',
            field=models.IntegerField(default=0),
        ),
    ]