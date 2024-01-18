from fightEvaluator.models import *
#for every event
#  for every matchup 
#    add the event date to the matchup

def add_dates():
    for fight_event in FightEvent.objects.all():
        for matchup in MatchUp.objects.filter(event=fight_event):
            matchup.scheduled = fight_event.date
            matchup.save()