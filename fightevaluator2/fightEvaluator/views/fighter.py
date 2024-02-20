from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,QueryDict
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST,require_GET,require_http_methods

from ..models import FightEvent,MatchUp,Fighter,Assessment,Note,WeightClass,Stance
from ..forms import *
import json
import datetime

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

@require_POST
def create_fighter(request):
    #get query params from request object
    fighterInput = json.loads(request.body)
    fighterInput['weight_class'] = fighterInput['weight_class'].lower()
    fighterForm = FighterForm(fighterInput)#validate data
    # print(fighterForm)
    if fighterForm.is_valid():
        print('fighter valid input')
        print(fighterForm.cleaned_data)
        fighterForm.save()#save fighter
    else:
        print('invalid fighter input')
    return JsonResponse({'fighter':model_to_dict(fighterForm.instance)})

@require_http_methods(["PATCH"])
def update_fighter(request,fighterId):
    fighter = get_object_or_404(Fighter,id=fighterId)
    #get query params from request object
    fighterInput = json.loads(request.body)
    #since attrs are optional we need to check if they exist
    #validate optional fields if they exist
    # print(fighterInput)
    form = FighterForm(fighterInput)
    if form.is_valid():
        # print('fighter valid input')
        # form.save(commit=True)#did this work?
        fighter.first_name = form.cleaned_data['first_name']
        fighter.last_name = form.cleaned_data['last_name']
        fighter.height = form.cleaned_data['height']
        fighter.weight_class = WeightClass[form.cleaned_data['weight_class'].upper()]
        fighter.reach = form.cleaned_data['reach']
        if form.cleaned_data['stance'] != None:
            fighter.stance = Stance[form.cleaned_data['stance'].upper()]
        fighter.date_of_birth = form.cleaned_data['date_of_birth']
        fighter.wins = form.cleaned_data['wins']
        fighter.losses = form.cleaned_data['losses']
        fighter.draws = form.cleaned_data['draws']
        fighter.img_link = form.cleaned_data['img_link']
        fighter.save()
    else:
        print('invalid fighter input')
        # return JsonResponse({'error':'invalid form'})

    return JsonResponse(getFighterJSON(fighter))


def getFighterJSON(fighter: Fighter):
    fighterjson = model_to_dict(fighter)
    if 'stance' in fighterjson and fighterjson['stance'] != None:
        fighterjson['stance'] = fighterjson['stance'].replace(' ','_').lower()
    fighterjson['weight_class'] = fighterjson['weight_class'].replace(' ','_').lower()
    if fighterjson['date_of_birth'] != None:
        fighterjson['date_of_birth'] = fighterjson['date_of_birth'].strftime('%Y-%m-%d')
    return fighterjson
