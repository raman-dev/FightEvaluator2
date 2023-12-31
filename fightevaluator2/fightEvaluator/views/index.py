from django.shortcuts import render
from django.views.decorators.http import require_GET

from ..models import FightEvent,MatchUp
from ..forms import *
import json
import datetime

# Create your views here.
@require_GET
def index(request):
    #purpose of index
    #show next upcoming fight event
    nextEvent = FightEvent.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
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
    
    context= {
        'event': nextEvent,
        'matchupsList': [mainCard,prelims],
    }

    return render(request, "fightEvaluator/index.html",context)



