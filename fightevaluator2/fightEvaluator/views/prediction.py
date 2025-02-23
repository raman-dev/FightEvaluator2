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
    
    calculate_stats()

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
    stats = {}
    stats['general'] = Stat.objects.filter(type=Stat.StatTypes.general)
    stats['fight_outcome'] = Stat.objects.filter(type=Stat.StatTypes.fight_outcome).order_by("-ratio")
    
    return stats

def calculate_stats():
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
    #fight outcome events
    outcomeStatObjs = Stat.objects.filter(type=Stat.StatTypes.fight_outcome)
    for event_name in Event.names:
        #if we have
        stat = outcomeStatObjs.filter(name=event_name).first()
        if stat:
            #how many predictions of this type
            result = Prediction.objects.aggregate(
                total=Count('isCorrect',filter=Q(prediction__event=Event[event_name])),
                correct=Count('isCorrect',filter=Q(prediction__event=Event[event_name],isCorrect=True))
            )
            stat.total = result['total']
            stat.count = result['correct']
            stat.ratio = stat.count/stat.total
            stat.save()
            # print(stat)
    
    all = Stat.objects.get(type='general')
    aggr = Prediction.objects.aggregate(
        total=Count('isCorrect'),
        count = Count('isCorrect',filter=Q(isCorrect=True))
        )
    all.total = aggr['total']
    all.count = aggr['count']
    all.ratio = all.count/all.total
    all.save()
    # print(all)
def stats(request): 
    return JsonResponse(getStats(),safe=False)