# Generated by Django 5.0 on 2024-02-05 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0048_matchupoutcome_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchupoutcome',
            name='outcome',
            field=models.CharField(choices=[('Win', 'Fighter wins'), ('Yes', 'Fight Goes the Distance'), ('No', 'Fight Does Not Go the Distance'), ('Rnds >= 0.5', 'Fight lasts more than 0.5 rounds'), ('Rnds >= 1.5', 'Fight lasts more than 1.5 rounds'), ('Rnds >= 2.5', 'Fight lasts more than 2.5 rounds'), ('Rnds >= 3.5', 'Fight lasts more than 3.5 rounds'), ('Rnds >= 4.5', 'Fight lasts more than 4.5 rounds')], max_length=256),
        ),
    ]