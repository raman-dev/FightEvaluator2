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
        total_win_type=Count('isCorrect',filter=Q(prediction__event=Event.WIN)),
        total_rounds_geq_one_half=Count('isCorrect',filter=Q(prediction__event=Event.ROUNDS_GEQ_ONE_AND_HALF)),
    )
    stats = {}
    stats['total_predictions']= data['correct'] + data['incorrect']
    stats['ratio'] = f"{data['correct']}/{stats['total_predictions']}"
    stats['accuracy_overall'] = f"{(100 * (data['correct']/stats['total_predictions'])):.2f}%"
    
    #WIN_TYPE_ACCURACY
    data.update(Prediction.objects.aggregate(
        win=Count('isCorrect',filter=Q(isCorrect=True,prediction__event=Event.WIN)),
        rounds_geq_one_half=Count('isCorrect',filter=Q(isCorrect=True,prediction__event=Event.ROUNDS_GEQ_ONE_AND_HALF))
    ))
    stats['win_type_ratio'] = f"{data['win']}/{data['total_win_type']}" 
    stats['win_type_accuracy'] = f"{(100 * (data['win']/data['total_win_type'])):.2f}%"
    stats['rounds_geq_one_half_ratio'] = f"{data['rounds_geq_one_half']}/{data['total_rounds_geq_one_half']}"
    stats['rounds_geq_one_half_accuracy']=f"{(100 * (data['rounds_geq_one_half']/data['total_rounds_geq_one_half'])):.2f}%"
    return stats

def stats(request):
    return JsonResponse(getStats(),safe=False)