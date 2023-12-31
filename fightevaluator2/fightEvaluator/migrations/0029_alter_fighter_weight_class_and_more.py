# Generated by Django 5.0 on 2023-12-21 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0028_matchup_weight_class_alter_fighter_weight_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fighter',
            name='weight_class',
            field=models.CharField(choices=[('N/A', 'Na'), ('Atomweight', 'Atomweight'), ('Strawweight', 'Strawweight'), ('Flyweight', 'Flyweight'), ('Bantamweight', 'Bantamweight'), ('Featherweight', 'Featherweight'), ('lightweight', 'Lightweight'), ('Welterweight', 'Welterweight'), ('Middleweight', 'Middleweight'), ('Light Heavyweight', 'Light Heavyweight'), ('Heavyweight', 'Heavyweight'), ('Catch weight', 'Catch Weight')], max_length=100),
        ),
        migrations.AlterField(
            model_name='matchup',
            name='weight_class',
            field=models.CharField(choices=[('N/A', 'Na'), ('Atomweight', 'Atomweight'), ('Strawweight', 'Strawweight'), ('Flyweight', 'Flyweight'), ('Bantamweight', 'Bantamweight'), ('Featherweight', 'Featherweight'), ('lightweight', 'Lightweight'), ('Welterweight', 'Welterweight'), ('Middleweight', 'Middleweight'), ('Light Heavyweight', 'Light Heavyweight'), ('Heavyweight', 'Heavyweight'), ('Catch weight', 'Catch Weight')], default='N/A', max_length=100),
        ),
    ]
