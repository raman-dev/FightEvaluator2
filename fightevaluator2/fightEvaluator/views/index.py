from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse

from ..models import FightEvent,MatchUp,FightOutcome,Prediction
from ..forms import FightEventForm,MatchUpFormMF
import json
import datetime
import re
from .. import scraper
# from ..scraper import getUpcomingFightEvent

@require_GET
def indexById(request,eventId):
    eventQuerySet = FightEvent.objects.filter(id=eventId)
    if not eventQuerySet:
        return JsonResponse({'error':'No such event with id: '+str(eventId)})
    event = eventQuerySet[0]
    matchups = MatchUp.objects.filter(event=event)
    mainCard = []
    prelims = []
    for matchup in matchups:
        # print(matchup.isprelim,matchup)
        if matchup.isprelim:
            prelims.append(matchup)
        else:
            mainCard.append(matchup)
    # if not FightOutcome.objects.filter(matchup=mainCard[0]):
        #results not generated but may be available for query
    context = {
        'event': event,
        'matchupsList': [mainCard,prelims],
    }

    return render(request, "fightEvaluator/index2.html",context)

# Create your views here.
@require_GET
def index(request):
    #purpose of index
    #show next upcoming fight event
    nextEvent = FightEvent.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    #compare current date and next event date
    if not nextEvent:
        fightEventData = scraper.getUpcomingFightEvent()
        fightEventForm = FightEventForm(fightEventData['eventData'])
        
        if not fightEventForm.is_valid():
            return JsonResponse({'fightEventForm':'FUCKED','error':fightEventForm.errors})
        nextEvent = fightEventForm.save()
        
        for matchup in fightEventData['matchups']:
            matchup['event'] = nextEvent
            # print(matchup)
            matchup['scheduled'] = nextEvent.date
            # print(matchup)
            matchupForm = MatchUpFormMF(matchup)
            if not matchupForm.is_valid():
                return JsonResponse({'MatchUpFormMF':'FUCKED','error':matchupForm.errors})
            matchupForm.save()
    #if next event is in the  past use webscraper to grab next event
    #retreive matchups for next event
    matchups = MatchUp.objects.filter(event=nextEvent)
    #split into main card and prelims
    mainCard = []
    prelims = []
    for matchup in matchups:
        if matchup.isprelim:
            prelims.append(matchup)
        else:
            mainCard.append(matchup)
    
    context = {
        'event': nextEvent,
        'matchupsList': [mainCard,prelims],
    }

    return render(request, "fightEvaluator/index2.html",context)

@require_GET
def events(request):
    #return a list of all events sorted by date
    events = FightEvent.objects.all().order_by('date').reverse()
    
    return render(request,"fightEvaluator/events.html",{'events':events})

def focusTest(request):
    return render(request,"fightEvaluator/focusTest.html",{})

def getFightEndMethod(rawIn):
    raw_method = rawIn.lower()
    if 'decision' in raw_method:
        return FightOutcome.Outcomes.DECISION
    if 'ko' in raw_method:
        return FightOutcome.Outcomes.KO
    if 'submission' in raw_method:
        return FightOutcome.Outcomes.SUBMISSION
    if 'no contest' in raw_method:
        return FightOutcome.Outcomes.NO_CONTEST
    if 'draw' in raw_method:
        return FightOutcome.Outcomes.DRAW
    
    return FightOutcome.Outcomes.NA

def getFightEndTimeAndRound(raw_time):
    #parsing time 
    #if all rounds are completed
    # print(raw_time)
    # time format -> 3/5 rounds, 15:00/25:00 Total
    rounds = 0
    time = ""
    if re.match(r'\d Rounds, \d{2}:\d{2} Total',raw_time):
        #get the rounds split on the comma
        rounds = re.search(r'\d',raw_time).group(0)#first number will be rounds
        time = re.search(r'\d{2}:\d{2}',raw_time).group(0)#second number will be time
    else:
    # time format -> 1:23 Round X of Y
        time = re.search(r'\d:\d{2}',raw_time).group(0)#first number will be time
        round_str = re.search(r'\d of \d',raw_time).group(0)#second number will be rounds
        rounds,_ = round_str.split('of')

    return time,int(rounds)


@require_GET
def getFightEventResults2(request,eventId):
    fightEvent = get_object_or_404(FightEvent,id=eventId)
    #do not try and get event results if the event is in the future
    #or if the it is not the atleast 2:00 am the day after the event
    if fightEvent.date > datetime.date.today() or datetime.datetime.now().hour < 2:
        return JsonResponse({'fightOutcomes':[],'error':'Results not available yet'})
    matchups = MatchUp.objects.filter(event=fightEvent)
    



#maybe asynchronous in the future evaluate
#fetch results from web if not already in database
@require_GET
def getFightEventResults(request,eventId):
    
    fightEvent = get_object_or_404(FightEvent,id=eventId)
    #do not try and get event results if the event is in the future
    #or if the it is not the atleast 2:00 am the day after the event
    if fightEvent.date > datetime.date.today() or datetime.datetime.now().hour < 2:
        return JsonResponse({'fightOutcomes':[],'error':'Results not available yet'})
    matchups = MatchUp.objects.filter(event=fightEvent)
    nameMatchupMap = {}
    
    fightOutcomes = []
    hasOutcomes = False
    for matchup in matchups:
        nameMatchupMap[matchup.fighter_a.name_unmod] = matchup
        nameMatchupMap[matchup.fighter_b.name_unmod] = matchup
        fightOutcome = FightOutcome.objects.filter(matchup=matchup).first()
        if fightOutcome:
            fightOutcomes.append(model_to_dict(fightOutcome))
            hasOutcomes = True
            
    if not hasOutcomes:
        # print(fightEvent.link)
        outcomes = scraper.getFightEventResults(fightEvent.link)
        # print(outcomes)
        for outcome in outcomes:
            #do what find the corresponding matchup from matchups
            raw_time = outcome['time']
            raw_method = outcome['method']
            fighter_0 = outcome['fighter_0']
            fighter_1 = outcome['fighter_1']

            if fighter_0 in nameMatchupMap:
                matchup = nameMatchupMap[fighter_0]
            if not matchup and not fighter_1 in nameMatchupMap:
                matchup = nameMatchupMap[fighter_1]
            if not matchup:#try other fighter name since names can be sometimes different on different sites
                # matchup = nameMatchupMap[fighter_1]
                continue#skip result
            winner = None
            if 'winner' in outcome:
                winner_name = outcome[outcome['winner']]
                #grab the fighter object from the matchup
                if winner_name == matchup.fighter_a.name_unmod:
                    winner = matchup.fighter_a
                else:
                    winner = matchup.fighter_b
            method = getFightEndMethod(raw_method)
            time,final_round = getFightEndTimeAndRound(raw_time)
            
            fightOutcome = FightOutcome(
                matchup=matchup,
                time=time,
                method=method,
                final_round=final_round,
                winner=winner
            )
            fightOutcome.save()
            fightOutcomes.append(model_to_dict(fightOutcome))
    # print(fightOutcomes)
    return JsonResponse({'fightOutcomes':fightOutcomes})

@require_GET
def event_predictions(request,eventId):
    #should be a list of predictions for matchups for event with eventId
    event = get_object_or_404(FightEvent,id=eventId)
    matchups = MatchUp.objects.filter(event=event)
    #for every matchup with a prediction
    predictions = []
    for matchup in matchups:
        prediction = Prediction.objects.filter(matchup=matchup).first()
        if prediction:
            predictions.append(prediction)
    
    return render(request,"fightEvaluator/event_predictions.html",{'predictions':predictions,'event':event})
    