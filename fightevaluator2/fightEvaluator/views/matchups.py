from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,QueryDict
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST,require_GET,require_http_methods

from ..models import FightEvent,MatchUp,Fighter,Assessment,Note,WeightClass,Stance
from ..forms import *
import json
import datetime

@require_GET
def matchup_index(request,matchupId):
    matchup = get_object_or_404(MatchUp,id=matchupId)
    attribComparison = []
    fighterA_assessment = model_to_dict(Assessment.objects.get(fighter=matchup.fighter_a))
    fighterB_assessment = model_to_dict(Assessment.objects.get(fighter=matchup.fighter_b))
    # print(fighterA_assessment)
    for k in fighterA_assessment.keys():
        if k == 'id' or k == 'fighter':
            continue            
        attribComparison.append((k,fighterA_assessment[k],fighterB_assessment[k]))
    # print(attribComparison)
    context = {
        'matchup':matchup,
        'fighter_a':matchup.fighter_a,
        'fighter_b':matchup.fighter_b,
        'fighter_a_notes':Note.objects.filter(assessment=Assessment.objects.get(fighter=matchup.fighter_a)).order_by('-createdAt'),
        'fighter_b_notes':Note.objects.filter(assessment=Assessment.objects.get(fighter=matchup.fighter_b)).order_by('-createdAt'),
        'attribComparison':attribComparison
    }
    return render(request,"fightEvaluator/matchup.html",context)

@require_POST
def create_matchup(request):
    #get body parameters from request object
    #convert body bytes to json object
    inputBody = json.loads(request.body)
    print(inputBody)
    form = MatchUpForm(inputBody)#use django form object for data validation
    #takes a querydict class as input querydict is a subclass of dict so a normal dict will suffice
    #create matchup
    matchup = None
    if form.is_valid():
        print('form is valid')    
        matchup = MatchUp(fighter_a=Fighter.objects.get(id=form.cleaned_data['fighter_a_id']),
                          fighter_b=Fighter.objects.get(id=form.cleaned_data['fighter_b_id']),#get fighter object from id
                          weight_class=form.cleaned_data['weight_class'],
                          rounds=form.cleaned_data['rounds'])
        if form.cleaned_data['scheduled'] != None:
            matchup.scheduled = datetime(form.cleaned_data['scheduled'])
        if form.cleaned_data['event_id'] != None:
            matchup.event = FightEvent.objects.get(id=form.cleaned_data['event_id'])
        if form.cleaned_data['isprelim'] != None:
            print('isprelim',form.cleaned_data['isprelim'])
            matchup.isprelim = form.cleaned_data['isprelim']
        matchup.save()
    else:
        #raise validation error
        print('invalid')
    return JsonResponse(model_to_dict(matchup))

@require_http_methods(["DELETE"])
def delete_matchup(request,matchupId):
    # MatchUp.objects.filter(id=matchupId).delete()#delete matchup with id
    #get object 404 if not found
    matchup = get_object_or_404(MatchUp,id=matchupId)
    matchup.delete()
    return JsonResponse({"success":"true"})
