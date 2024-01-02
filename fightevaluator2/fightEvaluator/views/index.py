from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..models import FightEvent,MatchUp
from ..forms import FightEventForm,MatchUpForm
import json
import datetime
from ..scraper import getUpcomingFightEvent

# Create your views here.
@require_GET
def index(request):
    #purpose of index
    #show next upcoming fight event
    nextEvent = FightEvent.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    #compare current date and next event date
    if not nextEvent:
        fightEventData = getUpcomingFightEvent()
        fightEventForm = FightEventForm(fightEventData.eventData)
        if not fightEventForm.is_valid():
            return render(request,"fightEvaluator/index.html",{'error':fightEventForm.errors})
        fightEventForm.save()
        nextEvent = fightEventForm.instance
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



