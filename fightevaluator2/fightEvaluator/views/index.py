from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import JsonResponse

from ..models import FightEvent,MatchUp
from ..forms import FightEventForm,MatchUpFormMF
import json
import datetime
from ..scraper import getUpcomingFightEvent

@require_GET
def indexById(request,eventId):
    event = FightEvent.objects.filter(id=eventId)[0]
    matchups = MatchUp.objects.filter(event=event)
    mainCard = []
    prelims = []
    for matchup in matchups:
        # print(matchup.isprelim,matchup)
        if matchup.isprelim:
            prelims.append(matchup)
        else:
            mainCard.append(matchup)
    
    context = {
        'event': event,
        'matchupsList': [mainCard,prelims],
    }

    return render(request, "fightEvaluator/index.html",context)

# Create your views here.
@require_GET
def index(request):
    #purpose of index
    #show next upcoming fight event
    nextEvent = FightEvent.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    #compare current date and next event date
    if not nextEvent:
        fightEventData = getUpcomingFightEvent()
        fightEventForm = FightEventForm(fightEventData['eventData'])
        
        if not fightEventForm.is_valid():
            return JsonResponse({'fightEventForm':'FUCKED','error':fightEventForm.errors})
        nextEvent = fightEventForm.save()
        
        for matchup in fightEventData['matchups']:
            matchup['event'] = nextEvent
            matchupForm = MatchUpFormMF(matchup)
            if not matchupForm.is_valid():
                return JsonResponse({'MatchUpFormMF':'FUCKED','error':matchupForm.errors})
            matchupForm.save()
    #if next event is in the  past use webscraper to grab next event
    #retreive matchups for next event
    matchups = MatchUp.objects.filter(event=nextEvent)
    #split into main card and prelims
    mainCard = []
    prelims = []
    for matchup in matchups:
        if matchup.isprelim:
            prelims.append(matchup)
        else:
            mainCard.append(matchup)
    
    context = {
        'event': nextEvent,
        'matchupsList': [mainCard,prelims],
    }

    return render(request, "fightEvaluator/index.html",context)



