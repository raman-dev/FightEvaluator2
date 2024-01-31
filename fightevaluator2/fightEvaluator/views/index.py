from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse

from ..models import FightEvent,MatchUp,FightOutcome
from ..forms import FightEventForm,MatchUpFormMF
import json
import datetime
import re
from ..scraper import getUpcomingFightEvent,getFightEventResults

@require_GET
def indexById(request,eventId):
    event = FightEvent.objects.filter(id=eventId)[0]
    matchups = MatchUp.objects.filter(event=event)
    mainCard = []
    prelims = []
    for matchup in matchups:
        # print(matchup.isprelim,matchup)
        if matchup.isprelim:
            prelims.append(matchup)
        else:
            mainCard.append(matchup)
    
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
        fightEventData = getUpcomingFightEvent()
        fightEventForm = FightEventForm(fightEventData['eventData'])
        
        if not fightEventForm.is_valid():
            return JsonResponse({'fightEventForm':'FUCKED','error':fightEventForm.errors})
        nextEvent = fightEventForm.save()
        
        for matchup in fightEventData['matchups']:
            matchup['event'] = nextEvent
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
#maybe asynchronous in the future evaluate
def getFightEventResults(request,eventId):
    fightEvent = get_object_or_404(FightEvent,id=eventId)
    matchups = MatchUp.objects.filter(event=fightEvent)
    nameMatchupMap = {}
    
    fightOutcomes = []
    hasOutcomes = False
    for matchup in matchups:
        nameMatchupMap[matchup.fighter_a.name_unmod] = matchup
        nameMatchupMap[matchup.fighter_b.name_unmod] = matchup
        fightOutcome = FightOutcome.objects.filter(matchup=matchup)
        if fightOutcome:
            fightOutcomes.append(fightOutcome)
            hasOutcomes = True
            
    if not hasOutcomes:
        outcomes = getFightEventResults(fightEvent.link)
        for outcome in outcomes:
            #do what find the corresponding matchup from matchups
            raw_time = outcome['time']
            raw_method = outcome['method']
            fighter_0 = outcome['fighter_0']
            fighter_1 = outcome['fighter_1']

            matchup = nameMatchupMap[fighter_0]
            if not matchup:#try other fighter name since names can be sometimes different on different sites
                matchup = nameMatchupMap[fighter_1]
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
            fightOutcomes.append(fightOutcome)
    
    return JsonResponse({'fightOutcomes':fightOutcomes})