from django.shortcuts import render,get_object_or_404
from .models import FightEvent,MatchUp,Fighter,WeightClass
from django.http import JsonResponse,QueryDict
from django.db.models import Q
from django.forms.models import model_to_dict
from django import forms
import json
import datetime


class MyForm(forms.Form):
    fname = forms.CharField(label='First Name', max_length=100)
    lname = forms.CharField(label='Last Name', max_length=100)

def test_post(request):
    print(request.headers)
    print(request.POST)
    print(request.body)

    return JsonResponse({'success':'true'})

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
        'form': MyForm(),
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


def create_fighter(request):
    #get query params from request object
    fname = request.GET.get('fname')
    lname = request.GET.get('lname')
    fighter = Fighter(first_name=fname,last_name=lname)
    fighter.save()
    return JsonResponse({'fighter':model_to_dict(fighter)})

class MatchUpForm(forms.Form):
    fighter_a_id = forms.IntegerField(label='Fighter A Id')
    fighter_b_id = forms.IntegerField(label='Fighter B Id')   
    weight_class = forms.CharField(label='Weight Class',max_length=100)
    rounds = forms.IntegerField(label='Rounds',initial=3)

    scheduled = forms.DateField(label='Scheduled',initial=None,required=False)
    event_id = forms.IntegerField(label='Event Id',initial=None,required=False)
    isprelim = forms.BooleanField(label='Is Prelim',initial=True,required=False)

    def is_valid(self) -> bool:
        return super().is_valid()


def create_matchup(request):
    #get body parameters from request object
    # print(request.headers)
    # print(request.body)
    # print(request.POST)
    # print(request.POST['fighter_a_id'])
    #convert body bytes to json object
    inputBody = json.loads(request.body)
    # queryDict = QueryDict()
    form = MatchUpForm(inputBody)
    # print(form) 
    # print(queryDict['fighter_a_id'])
    # fighter_a_id = inputBody['fighter_a_id']
    # fighter_b_id = inputBody['fighter_b_id']
    # weight_class = inputBody['weight_class']
    # rounds = inputBody['rounds']
    # #optional parameters
    # scheduled = None
    # event_id = None
    # isprelim = None

    # if 'scheduled' in inputBody:
    #     scheduled = inputBody['scheduled'] #if scheduled is empty string then it will be None
    # if 'event_id' in inputBody:
    #     event_id = inputBody['event_id']#if event_id is present
    # if 'isprelim' in inputBody:
    #     isprelim = inputBody['isprelim']#if present
    # #print read in parameters
    # print(fighter_a_id,fighter_b_id,weight_class,rounds,scheduled,event_id,isprelim)
    #create matchup
    #matchup = MatchUp(fighter_a=Fighter.objects.get(id=fighter_a_id),
    #                   fighter_b=Fighter.objects.get(id=fighter_b_id),#get fighter object from id
    #                   weight_class=weight_class,
    #                   rounds=rounds,
    #                   scheduled=datetime.date(scheduled),
    #                   event=FightEvent.objects.get(id=event_id),
    #                   isprelim=isprelim)
    return JsonResponse({'matchup':{}})

def delete_matchup(request,matchupId):
    # MatchUp.objects.filter(id=matchupId).delete()#delete matchup with id
    #get object 404 if not found
    matchup = get_object_or_404(MatchUp,id=matchupId)
    matchup.delete()
    return JsonResponse({"success":"true"})