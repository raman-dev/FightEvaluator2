from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse

from ..models import FightEvent,MatchUp,FightOutcome,Prediction,Event
from ..forms import FightEventForm,MatchUpFormMF
import json
import datetime
import re
from .. import scraper

def predictions(request):
    
    """
        structure {   
            matchup : String,
            prediction : String
            isCorrect : boolean
            isGamble : boolean
        }
    """
    context = {
        'predictions':Prediction.objects.all()
    }

    return render(request, "fightEvaluator/prediction.html",context)

def publishResults(request):
    #using matchup results determine if predictions are correct
    #for every prediction grab the corresponding fightResult if it exists
    for prediction in Prediction.objects.all():
        outcome = FightOutcome.objects.filter(matchup=prediction.matchup).first()
        if outcome:
            #print(prediction,outcome)
            #do what now hello
            #if prediction has a fighter then it is a winner determination
            match prediction.prediction.event:
                case Event.DOES_NOT_GO_THE_DISTANCE:
                    print("")
                case Event.ROUNDS_GEQ_ONE_AND_HALF:
                    if outcome.final_round > 2:
                        prediction.isCorrect = True
                    elif outcome.final_round == 2:
                        #time is str
                        #int:int
                        seconds = 30#
                        _,actual_seconds = outcome.time.split(":")
                        if seconds >= actual_seconds:
                            prediction.isCorrect = True
                case Event.WIN:
                    if outcome.winner != None and prediction.prediction.fighter == outcome.winner:
                        prediction.isCorrect = True

        prediction.save()
        print(prediction,prediction.isCorrect)
    return JsonResponse({"hello":"world"})