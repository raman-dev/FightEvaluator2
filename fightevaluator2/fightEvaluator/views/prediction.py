from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Avg,Count,Q,Sum
from django.views.decorators.cache import cache_page

from ..models import FightEvent,FightOutcome,Prediction,Event,Likelihood,Stat,EventStat,MonthlyEventStats
from rich import print as rprint

from datetime import datetime

@cache_page(60* 2)  # Cache the view for 2 mins
@require_GET
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
    # calculate_stats()
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


@cache_page(60* 2)  # Cache the view for 15 minutes
@require_GET
def getPredictions(request):
    
    print("Running predictions view")
    predictions = []
    """

        select *
        from
            prediction
        order by
            date.month
        group by
        
        predictions: [
            {  
                event: data
                predictions:[
                
                ]
            }
        ]

    """
    # calculate_stats()
    events = FightEvent.objects.all().order_by('-date')# prepend negative to get reverse ordering
    data = Prediction.objects.all()
    # eventsByYearMonth = {}
    for fightEvent in events:
        #grab predictions for this event
        preds = data.filter(matchup__event=fightEvent)
        if preds.count() > 0:#atleast 1 prediction for this event
             predictions.append({
                 'event':model_to_dict(fightEvent),
                 'predictions': [ {
                     'matchup':p.matchup.title(),
                     'type':p.prediction.event,
                     'type_label':p.prediction.get_event_display(),
                     'likelihood':p.prediction.likelihood,
                     'fighter': p.prediction.fighter.name if p.prediction.fighter else None,
                     'correct':p.isCorrect
                 } for p in preds]
            })

    return JsonResponse({'predictions':predictions})

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

    collect_monthly_stats()
    # print(all)

def collect_monthly_stats(year=None, month=None):
    """
    Collect stats for a given year and month.
    Defaults to the current month if none provided.
    Returns: (monthly_stats_object, created_bool)
    """
    if year is None or month is None:
        today = datetime.today()
        year = year or today.year
        month = month or today.month

    # filter events in the target month
    event_stats = EventStat.objects.filter(
        event__date__year=year,
        event__date__month=month,
    )

    # aggregate totals
    aggregates = event_stats.aggregate(
        total_events=Count("event", distinct=True),
        total_predictions=Sum("predictions"),
        total_correct=Sum("correct"),
    )

    # handle None values
    events = aggregates["total_events"] or 0
    predictions = aggregates["total_predictions"] or 0
    correct = aggregates["total_correct"] or 0

    # create or update the MonthlyEventStats record
    monthly_stats, created = MonthlyEventStats.objects.update_or_create(
        year=year,
        month=month,
        defaults={
            "events": events,
            "predictions": predictions,
            "correct": correct,
        },
    )

    return monthly_stats, created

def stats(request): 
    return JsonResponse(getStats(),safe=False)