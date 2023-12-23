# Generated by Django 5.0 on 2023-12-19 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightEvaluator', '0016_alter_note_createdat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(blank=True, max_length=256, null=True)),
                ('tag', models.IntegerField(choices=[(0, 'Untested'), (1, 'Negative'), (2, 'Neutral'), (3, 'Positive')], default=2)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FightEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MatchUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled', models.DateField(default=None, null=True)),
                ('event', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fightEvaluator.fightevent')),
                ('fighter_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter_a', to='fightEvaluator.fighter')),
                ('fighter_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighter_b', to='fightEvaluator.fighter')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentNote',
            fields=[
                ('note2_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fightEvaluator.note2')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fightEvaluator.assessment')),
            ],
            bases=('fightEvaluator.note2',),
        ),
        migrations.CreateModel(
            name='MatchupNote',
            fields=[
                ('note2_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fightEvaluator.note2')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fightEvaluator.matchup')),
            ],
            bases=('fightEvaluator.note2',),
        ),
    ]