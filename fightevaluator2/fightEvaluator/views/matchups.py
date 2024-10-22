from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,QueryDict
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST,require_GET,require_http_methods

from ..models import FightEvent,MatchUp,Fighter,Assessment,Note,FightOutcome,EventLikelihood,Event,Likelihood,Prediction
from ..forms import *
import json
import datetime
from rich import print as rprint


@require_GET
def matchup_index(request,matchupId):
    matchup = get_object_or_404(MatchUp,id=matchupId)
    # Prediction = Prediction.objects.filter(matchup=matchup).first()

    attribComparison = []
    fighterA_assessment = model_to_dict(Assessment.objects.get(fighter=matchup.fighter_a))
    fighterB_assessment = model_to_dict(Assessment.objects.get(fighter=matchup.fighter_b))
    # print(fighterA_assessment)
    for k in fighterA_assessment.keys():
        if k == 'id' or k == 'fighter':
            continue            
        attribComparison.append((k,fighterA_assessment[k],fighterB_assessment[k]))
    result = FightOutcome.objects.filter(matchup=matchup).first()
    context = {
        'matchup':matchup,
        'fighter_a':matchup.fighter_a,
        'fighter_b':matchup.fighter_b,
        'fighter_a_notes':Note.objects.filter(assessment=Assessment.objects.get(fighter=matchup.fighter_a)).order_by('-createdAt'),
        'fighter_b_notes':Note.objects.filter(assessment=Assessment.objects.get(fighter=matchup.fighter_b)).order_by('-createdAt'),
        'attribComparison':attribComparison,
        'standardEvents':[
            (Event.WIN,matchup.fighter_a.id),
            (Event.WIN,matchup.fighter_b.id),
            (Event.ROUNDS_GEQ_ONE_AND_HALF,None),
            (Event.DOES_NOT_GO_THE_DISTANCE,None)],
        'eventLikelihoods':EventLikelihood.objects.filter(matchup=matchup),
        'prediction':Prediction.objects.filter(matchup=matchup).first(),
    }
    if result:
        context['result'] = {
            'method':result.method,
            'final_round':result.final_round,
            'time':result.time,
        }
        if result.winner:
            context['result']['winner_id'] = result.winner.id
    return render(request,"fightEvaluator/matchup2.html",context)

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
        print('invalid',form.errors)
        return JsonResponse({"fuck":"me"})
    responseDict = model_to_dict(matchup)
    responseDict['fighter_a_name'] = matchup.fighter_a.name
    responseDict['fighter_b_name'] = matchup.fighter_b.name
    return JsonResponse(responseDict)

@require_http_methods(["DELETE"])
def delete_matchup(request,matchupId):
    # MatchUp.objects.filter(id=matchupId).delete()#delete matchup with id
    #get object 404 if not found
    matchup = get_object_or_404(MatchUp,id=matchupId)
    matchup.delete()
    return JsonResponse({"success":"true"})

@require_http_methods(["PATCH"])
def update_matchup(request,matchupId):
    matchup = get_object_or_404(MatchUp,id=matchupId)
    inputBody = json.loads(request.body)
    
    matchupUpdateForm = MatchUpForm(inputBody)
    if matchupUpdateForm.is_valid():
        matchup.fighter_a = Fighter.objects.get(id=matchupUpdateForm.cleaned_data['fighter_a_id'])
        matchup.fighter_b = Fighter.objects.get(id=matchupUpdateForm.cleaned_data['fighter_b_id'])
        matchup.weight_class = matchupUpdateForm.cleaned_data['weight_class']
        matchup.rounds = matchupUpdateForm.cleaned_data['rounds']
        matchup.scheduled = matchupUpdateForm.cleaned_data['scheduled']
        matchup.isprelim = matchupUpdateForm.cleaned_data['isprelim']
        matchup.save()
    else:
        return JsonResponse({"success":"false","errors":matchupUpdateForm.errors})

    return JsonResponse(model_to_dict(matchup))


@require_http_methods(["PATCH"])
def toggle_watchlist(request,matchupId):
    matchup = get_object_or_404(MatchUp,id=matchupId)
    matchup.inWatchList = not matchup.inWatchList
    matchup.save()
    return JsonResponse(model_to_dict(matchup))

@require_http_methods(["PUT"])
def updateMatchUpEventLikelihood(request):
    inputBody = json.loads(request.body)
    matchup = get_object_or_404(MatchUp,id=inputBody['matchupId'])#need valid matchup id
    eventLikelihoodForm = MatchUpEventLikelihoodForm(inputBody)
    # print(inputBody,matchup)
    if eventLikelihoodForm.is_valid():
        #check if fighterId is valid 
        fighterId = eventLikelihoodForm.cleaned_data['fighterId']
        eventType = eventLikelihoodForm.cleaned_data['eventType']
        likelihood = eventLikelihoodForm.cleaned_data['likelihood']
        justification = eventLikelihoodForm.cleaned_data['justification']
        #if fighterId is valid this is a fighter specific event
        #else it is a general event which are unique for each matchup
        if fighterId != 0:
            fighter = Fighter.objects.get(id=fighterId)
            eventLikelihood = EventLikelihood.objects.filter(matchup=matchup,fighter=fighter,eventType=eventType).first()
            if eventLikelihood == None:
                eventLikelihood = EventLikelihood(matchup=matchup,fighter=fighter,event=Event[eventType],eventType=eventType)
                eventLikelihood.save()
            eventLikelihood.likelihood = likelihood
            eventLikelihood.justification = justification
            eventLikelihood.save()
            return JsonResponse({
                'id':eventLikelihood.id,
                'eventType':eventLikelihood.eventType,
                'likelihood':eventLikelihood.likelihood,
                'likelihood_display':eventLikelihood.get_likelihood_display(),
                'justification':eventLikelihood.justification,
                'fighterId':eventLikelihood.fighter.id
            })
        #general event
        eventLikelihood = EventLikelihood.objects.filter(matchup=matchup,eventType=eventType).first()
        if eventLikelihood == None:
            eventLikelihood = EventLikelihood(matchup=matchup,event=Event[eventType],eventType=eventType)
            eventLikelihood.save()
        eventLikelihood.likelihood = likelihood
        eventLikelihood.justification = justification
        eventLikelihood.save()
        return JsonResponse({
            'id':eventLikelihood.id,
            'eventType':eventLikelihood.eventType,
            'likelihood':eventLikelihood.likelihood,
            'justification':eventLikelihood.justification,
            'likelihood_display':eventLikelihood.get_likelihood_display(),
        })
    return JsonResponse({"success":"false","errors":eventLikelihoodForm.errors})

@require_http_methods(["PUT"])
def updateMatchUpEventPrediction(request):
    inputBody = json.loads(request.body)
    matchup = get_object_or_404(MatchUp,id=inputBody['matchupId'])
    #we want to create a new event likelihood if it does not exist
    #if it exists we want to query it
    # print(inputBody)
    eventPredictionForm = EventPredictionForm(inputBody)
    if eventPredictionForm.is_valid():
        fighterId = eventPredictionForm.cleaned_data['fighterId']
        eventType = eventPredictionForm.cleaned_data['eventType']
        if (fighterId == 0 and eventType == "NA"):
            #unset the prediction
            currentPrediction = Prediction.objects.filter(matchup=matchup).first()
            if currentPrediction != None:
                currentPrediction.delete()
            return JsonResponse({"success":"true"})
        
        eventLikelihood = EventLikelihood.objects.filter(matchup=matchup,eventType=eventType)
        currentPrediction = Prediction.objects.filter(matchup=matchup).first()
        if fighterId != 0:
            #fighter specific event
            fighter = Fighter.objects.get(id=fighterId)
            eventLikelihood = eventLikelihood.filter(fighter=fighter).first()
            if eventLikelihood == None:
                eventLikelihood = EventLikelihood(matchup=matchup,fighter=fighter,event=Event[eventType],eventType=eventType, likelihood = Likelihood.NEUTRAL)
                eventLikelihood.save()
        else:
            #general event
            eventLikelihood = eventLikelihood.first()
            if eventLikelihood == None:
                eventLikelihood = EventLikelihood(matchup=matchup,event=Event[eventType],eventType=eventType,likelihood=Likelihood.NEUTRAL)
                eventLikelihood.save()
        if currentPrediction == None:
            currentPrediction = Prediction(matchup=matchup,prediction=eventLikelihood)
            currentPrediction.save()
        else:
            currentPrediction.prediction = eventLikelihood
            currentPrediction.save()
        return JsonResponse({'eventType':currentPrediction.prediction.eventType,
                             'fighterId':fighterId})
    return JsonResponse({"success":"false","errors":eventPredictionForm.errors})
            

            