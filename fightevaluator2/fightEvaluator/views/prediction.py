from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Count,Q

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
    # context = {
    #     'predictions':Prediction.objects.all()
    # }
    # context = {}
    eventPredictionMap = {}
    for p in Prediction.objects.all():
        if p.matchup.event in eventPredictionMap:
            eventPredictionMap[p.matchup.event].append(p)
        else:
            eventPredictionMap[p.matchup.event] = []
            eventPredictionMap[p.matchup.event].append(p)
    predictionsByEvent = list(eventPredictionMap.items())
    predictionsByEvent.sort(key=lambda x: x[0].date)
    predictionsByEvent.reverse()
    return render(request, "fightEvaluator/prediction.html",{'event_predictions':predictionsByEvent,'stats':getStats()})

def verifyPrediction(matchups):
    for matchup in matchups:
        prediction = Prediction.objects.filter(matchup=matchup).first()
        if prediction:
            outcome = matchup.outcome
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
    return JsonResponse({"hello":"world"})

def getStats():

    #for all predictions get per event rate
    #get overall rate
    data = Prediction.objects.aggregate(
        correct=Count('isCorrect',filter=Q(isCorrect=True)),
        incorrect=Count('isCorrect',filter=Q(isCorrect=False)),
    )
    stats = {}
    stats['general']={}
    stats['general']['total_predictions']= data['correct'] + data['incorrect']
    stats['general']['ratio'] = f"{data['correct']}/{stats['general']['total_predictions']}"
    stats['general']['accuracy_overall'] = f"{(100 * (data['correct']/stats['general']['total_predictions'])):.2f}%"

    stats['prediction_type'] = {}

    for predictionEventType in Event:
        result = Prediction.objects.aggregate(
            total=Count('isCorrect',filter=Q(prediction__event=predictionEventType)),
            count=Count('isCorrect',filter=Q(isCorrect=True,prediction__event=predictionEventType))
        )
        if result['total'] == 0:
            continue
        stats['prediction_type'][predictionEventType] = {
            'ratio': f"{result['count']}/{result['total']}", 
            'accuracy':f"{(100 * (result['count']/result['total'])):.2f}%"
        }

    return stats

def stats(request):
    return JsonResponse(getStats(),safe=False)