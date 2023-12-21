from django.shortcuts import render
from .models import FightEvent,MatchUp,Fighter
from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict
import datetime

# Create your views here.
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

#search for a fighter
def fighter_search(request):
    #get query params from request object
    search_names = request.GET.get('search').split(' ')
    fname = search_names[0]
    lname = fname
    
    if len(search_names) > 1:
        lname = search_names[1]

    fighterQueryValues = ["id","first_name","last_name"]
    query = Q(first_name__startswith=fname) | Q(last_name__contains=lname)
    if fname != lname:
        query = Q(first_name__startswith=fname) & Q(last_name__contains=lname)
        # fighters = Fighter.objects.filter(Q(first_name__startswith=fname) | Q(last_name__contains=lname))[:5].values(fighterQueryValues)
    # else:
        # fighters = Fighter.objects.filter(first_name__startswith=fname,last_name__contains=lname)[:5].values()
    fighters = Fighter.objects.filter(query)[:5].values(*fighterQueryValues)#*list means non keyword arguments passed in
    return JsonResponse({'fighters':list(fighters)})