# Generated by Django 5.1.2 on 2024-11-21 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0071_matchup_fighter_a_references_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OddsDataState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staleOrEmpty', models.BooleanField(default=False)),
                ('updating', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='matchup',
            name='fighter_a_references',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='matchup',
            name='fighter_b_references',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]