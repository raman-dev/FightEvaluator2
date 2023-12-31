# Generated by Django 5.0 on 2023-12-21 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0027_alter_matchup_isprelim'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup',
            name='weight_class',
            field=models.CharField(choices=[('N/A', 'Na'), ('Atomweight', 'Atomweight'), ('Strawweight', 'Strawweight'), ('Flyweight', 'Flyweight'), ('Bantamweight', 'Bantamweight'), ('Featherweight', 'Featherweight'), ('Lightweight', 'Lightweight'), ('Welterweight', 'Welterweight'), ('Middleweight', 'Middleweight'), ('Light Heavyweight', 'Light Heavyweight'), ('Heavyweight', 'Heavyweight'), ('Catch weight', 'Catch Weight')], default='N/A', max_length=100),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='weight_class',
            field=models.CharField(choices=[('N/A', 'Na'), ('Atomweight', 'Atomweight'), ('Strawweight', 'Strawweight'), ('Flyweight', 'Flyweight'), ('Bantamweight', 'Bantamweight'), ('Featherweight', 'Featherweight'), ('Lightweight', 'Lightweight'), ('Welterweight', 'Welterweight'), ('Middleweight', 'Middleweight'), ('Light Heavyweight', 'Light Heavyweight'), ('Heavyweight', 'Heavyweight'), ('Catch weight', 'Catch Weight')], max_length=100),
        ),
    ]
