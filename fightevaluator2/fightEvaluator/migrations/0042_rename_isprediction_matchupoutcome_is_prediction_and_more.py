# Generated by Django 5.0 on 2024-01-24 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0041_matchupoutcome_isprediction_matchupoutcome_isresult_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchupoutcome',
            old_name='isprediction',
            new_name='is_prediction',
        ),
        migrations.RenameField(
            model_name='matchupoutcome',
            old_name='isresult',
            new_name='is_result',
        ),
    ]
