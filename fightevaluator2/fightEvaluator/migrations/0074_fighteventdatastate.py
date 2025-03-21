# Generated by Django 5.1.2 on 2024-11-23 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0073_oddsdatastate_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='FightEventDataState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staleOrEmpty', models.BooleanField(default=False)),
                ('updating', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
    ]
