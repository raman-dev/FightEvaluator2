# Generated by Django 5.1.2 on 2025-02-25 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0117_alter_eventlikelihood_event_alter_odd_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlikelihood',
            name='event',
            field=models.CharField(choices=[('Win', 'Fighter wins'), ('Yes', 'Fight Goes the Distance'), ('No', 'Fight Does Not Go the Distance'), ('Rnds >= 0.5', 'Fight lasts more than 0.5 rounds'), ('Rnds >= 1.5', 'Fight lasts more than 1.5 rounds'), ('Rnds >= 2.5', 'Fight lasts more than 2.5 rounds'), ('Rnds >= 3.5', 'Fight lasts more than 3.5 rounds'), ('Rnds >= 4.5', 'Fight lasts more than 4.5 rounds'), ('NA', 'Not Available')], max_length=256),
        ),
        migrations.AlterField(
            model_name='odd',
            name='event',
            field=models.CharField(choices=[('Win', 'Fighter wins'), ('Yes', 'Fight Goes the Distance'), ('No', 'Fight Does Not Go the Distance'), ('Rnds >= 0.5', 'Fight lasts more than 0.5 rounds'), ('Rnds >= 1.5', 'Fight lasts more than 1.5 rounds'), ('Rnds >= 2.5', 'Fight lasts more than 2.5 rounds'), ('Rnds >= 3.5', 'Fight lasts more than 3.5 rounds'), ('Rnds >= 4.5', 'Fight lasts more than 4.5 rounds'), ('NA', 'Not Available')], max_length=256),
        ),
        migrations.AlterField(
            model_name='pick',
            name='event',
            field=models.CharField(blank=True, choices=[('Win', 'Fighter wins'), ('Yes', 'Fight Goes the Distance'), ('No', 'Fight Does Not Go the Distance'), ('Rnds >= 0.5', 'Fight lasts more than 0.5 rounds'), ('Rnds >= 1.5', 'Fight lasts more than 1.5 rounds'), ('Rnds >= 2.5', 'Fight lasts more than 2.5 rounds'), ('Rnds >= 3.5', 'Fight lasts more than 3.5 rounds'), ('Rnds >= 4.5', 'Fight lasts more than 4.5 rounds'), ('NA', 'Not Available')], default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='prediction2',
            name='event',
            field=models.CharField(choices=[('Win', 'Fighter wins'), ('Yes', 'Fight Goes the Distance'), ('No', 'Fight Does Not Go the Distance'), ('Rnds >= 0.5', 'Fight lasts more than 0.5 rounds'), ('Rnds >= 1.5', 'Fight lasts more than 1.5 rounds'), ('Rnds >= 2.5', 'Fight lasts more than 2.5 rounds'), ('Rnds >= 3.5', 'Fight lasts more than 3.5 rounds'), ('Rnds >= 4.5', 'Fight lasts more than 4.5 rounds'), ('NA', 'Not Available')], max_length=256),
        ),
    ]
