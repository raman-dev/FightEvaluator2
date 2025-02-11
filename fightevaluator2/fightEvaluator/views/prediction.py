from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Avg,Count,Q

from ..models import FightEvent,FightOutcome,Prediction,Event,Likelihood,Stat
from rich import print as rprint

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
    
    data = Prediction.objects.all()
    # eventsByYearMonth = {}
    for fightEvent in events:
        #grab predictions for this event
        preds = data.filter(matchup__event=fightEvent)
        if preds.count() > 0:#atleast 1 prediction for this event
            eventPredictionMap[fightEvent] = preds
    return render(request, "fightEvaluator/prediction.html",{
        'event_predictions':eventPredictionMap,
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
    # data = Prediction.objects.aggregate(
    #     avg_correct=Avg('isCorrect'),
    #     correct=Count('isCorrect',filter=Q(isCorrect=True)),
    #     incorrect=Count('isCorrect',filter=Q(isCorrect=False)),
    #     very_likely=Count('isCorrect',filter=Q(prediction__likelihood=Likelihood.VERY_LIKELY)),
    #     very_likely_correct=Count('isCorrect',filter=Q(isCorrect=True,prediction__likelihood=Likelihood.VERY_LIKELY)),
    # )
    # """
    #     name: fighter_wins
    #     type = outcome
    #     count: num
    #     total: num + rest


    # """
    stats = {}
    # stats['general']={}
    # stats['general']['total_predictions']= data['correct'] + data['incorrect']
    # stats['general']['ratio'] = f"{data['correct']}/{stats['general']['total_predictions']}"
    # #data['correct']/stats['general']['total_predictions']
    # stats['general']['accuracy_overall'] = f"{(100 * (data['avg_correct'])):.2f}%"

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
    stats['general'] = Stat.objects.filter(type=Stat.StatTypes.general)
    stats['fight_outcome'] = Stat.objects.filter(type=Stat.StatTypes.fight_outcome).order_by("-ratio")
    # stats['probability'] = Stat.objects.filter(type=Stat.StatTypes.probability)
    # stats['predictionTypeStats'] = {}
    # stats['predictionLikelihoodStats'] = {}
    # """
    #     for every prediction_type get the corresponding ratio and accuracy
    # """
    
    # for predictionEventType in Event:
    #     result = Prediction.objects.aggregate(
    #         total=Count('isCorrect',filter=Q(prediction__event=predictionEventType)),
    #         count=Count('isCorrect',filter=Q(isCorrect=True,prediction__event=predictionEventType))
    #     )
    #     if result['total'] == 0:
    #         continue
    #     stats['predictionTypeStats'][predictionEventType.label] = {
    #         'ratio': f"{result['count']}/{result['total']}", 
    #         'accuracy':f"{(100 * (result['count']/result['total'])):.2f}%"
    #     }

    # for likelihood in Likelihood.choices:
    #     rprint(likelihood)
    #     result = Prediction.objects.aggregate(
    #         total=Count('isCorrect',filter=Q(prediction__likelihood=likelihood[0])),
    #         count=Count('isCorrect',filter=Q(isCorrect=True,prediction__likelihood=likelihood[0]))
    #     )
    #     if result['total'] == 0:
    #         continue
        
    #     rprint(result['total'],result['count'])
    #     stats['predictionTypeStats'][likelihood[1]] = {
    #         'ratio': f"{result['count']}/{result['total']}", 
    #         'accuracy':f"{(100 * (result['count']/result['total'])):.2f}%"
    #     }
    # rprint(stats)
    return stats

def stats(request):
    return JsonResponse(getStats(),safe=False)