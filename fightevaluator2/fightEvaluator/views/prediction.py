from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Avg,Count,Q
from django.db.models.functions import ExtractMonth,ExtractYear

from ..models import FightEvent,MatchUp,FightOutcome,Prediction,Event,Likelihood
from ..forms import FightEventForm,MatchUpFormMF
import json
import datetime
import re
from rich import print as rprint

from .. import scraper

def predictions(request):
    
    """
        structure 
            matchup : model_obj,
            prediction : String
            isCorrect : boolean
            isGamble : boolean
        
    """
    eventPredictionMap = {}
    """

        select *
        from
            prediction
        order by
            date.month
        group by
            

    """
    events = FightEvent.objects.all().order_by('-date')# prepend negative to get reverse ordering
    # years = Prediction.objects.annotate(year=ExtractYear('matchup__event__date')).values('year').distinct()#query set of years of predictions
    
    # rprint(years)
    
    data = Prediction.objects
    # eventsByYearMonth = {}
    for fightEvent in events:
        #grab predictions for this event
        preds = data.filter(matchup__event=fightEvent)
        if preds.count() > 0:#atleast 1 prediction for this event
            eventPredictionMap[fightEvent] = preds
            # eventsByYearMonth[currDate.year][currDate.month][fightEvent] = preds
    # rprint(eventsByYearMonth)
    # stats = {}
    #for every year
    # for yearMapping in data.annotate(year=ExtractYear('matchup__event__date')).values('year').distinct():
    #     currYear = yearMapping['year']
    #     rprint('Current Year => ',currYear)
    #     eventsThisYear = data.filter(matchup__event__date__year=currYear)
    #     #for every month
    #     stats[currYear] = {}
    #     for i in range(1,12 + 1):
    #         monthQ = Q(matchup__event__date__month=i)
    #         eventsThisMonth = eventsThisYear.filter(monthQ)
    #         monthlyStats = (eventsThisMonth.aggregate(
    #             total=Count("isCorrect"),
    #             correct=Count("isCorrect",filter=Q(isCorrect=True)),
    #         ))
    #         monthlyStats['incorrect'] = monthlyStats['total'] - monthlyStats['correct']
    #         #grab all events in this month
    #         stats[currYear][i] = monthlyStats

    # rprint(monthlyStats)
    # for event,predictions in eventPredictionMap.items():
        
    #     if currentYear != event.date.year:
    #         currentYear = event.date.year
    #         yearMap[currentYear] = {}
        
    #     if currentMonth != event.date.month:
    #         currentMonth = event.date.month
    #         yearMap[currentYear][currentMonth] = {}

    #     if event not in yearMap[currentYear][currentMonth]:
    #         yearMap[currentYear][currentMonth][event] = []
        
    #     yearMap[currentYear][currentMonth][event] = predictions
    # rprint(yearMap)
    return render(request, "fightEvaluator/prediction.html",{
        'event_predictions':eventPredictionMap,
        # 'predictionsByYearMonth':yearMap,
        'stats':getStats()
        })

def verifyPrediction(matchups):
    for matchup in matchups:
        prediction = Prediction.objects.filter(matchup=matchup).first()
        if prediction:
            outcome = matchup.outcome
            #if prediction has a fighter then it is a winner determination
            match prediction.prediction.event:
                case Event.DOES_NOT_GO_THE_DISTANCE:
                    #as long as outcome was ko or sub
                    prediction.isCorrect = outcome.method != FightOutcome.Outcomes.DECISION
                    prediction.isCorrect &= outcome.method != FightOutcome.Outcomes.DRAW 
                    prediction.isCorrect &= outcome.method != FightOutcome.Outcomes.NO_CONTEST
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
        avg_correct=Avg('isCorrect'),
        correct=Count('isCorrect',filter=Q(isCorrect=True)),
        incorrect=Count('isCorrect',filter=Q(isCorrect=False)),
        very_likely=Count('isCorrect',filter=Q(prediction__likelihood=Likelihood.VERY_LIKELY)),
        very_likely_correct=Count('isCorrect',filter=Q(isCorrect=True,prediction__likelihood=Likelihood.VERY_LIKELY)),
    )
    stats = {}
    stats['general']={}
    stats['general']['total_predictions']= data['correct'] + data['incorrect']
    stats['general']['ratio'] = f"{data['correct']}/{stats['general']['total_predictions']}"
    #data['correct']/stats['general']['total_predictions']
    stats['general']['accuracy_overall'] = f"{(100 * (data['avg_correct'])):.2f}%"

    """
        
        stats <---changes when a prediction object then has a corresponding outcome object
            overall:
                correctness 
                    ratio
                    percent
            event_type_x:  
                correctness 
                    ratio
                    percent
            likelihood_x:
                correctness
                    ratio
                    percent
        
        
        month: 
            correct_predictions/total_predictions
        
    """

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