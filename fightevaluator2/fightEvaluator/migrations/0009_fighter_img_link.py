# Generated by Django 5.0 on 2023-12-18 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0008_alter_fighter_weight_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='img_link',
            field=models.CharField(max_length=256, null=True),
        ),
    ]