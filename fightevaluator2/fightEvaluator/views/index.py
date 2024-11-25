from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse

from ..models import FightEvent,MatchUp,FightOutcome,Prediction,Event,FightEventDataState
from ..forms import FightEventForm,MatchUpFormMF
import json
import datetime
import re
from .. import scraper
from threading import Thread
from datetime import datetime
# from ..scraper import getUpcomingFightEvent

WorkerThread = None

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

    return render(request, "fightEvaluator/index3.html",context)

def WorkerThreadControlFunction():
    
    print('WorkerThread running....')
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
    fightEventDataState = FightEventDataState.objects.select_for_update().first()
    fightEventDataState.staleOrEmpty = False
    fightEventDataState.updating = False
    fightEventDataState.date = datetime.today().date()
    fightEventDataState.save()
    print('WorkerThread complete....')

def matchupDictWithName(matchup: MatchUp):
    
    name_a = matchup.fighter_a.name_unmod
    name_b = matchup.fighter_b.name_unmod
    
    result = model_to_dict(matchup)
    result['fighter_a_name'] = name_a
    result['fighter_b_name'] = name_b
    result['title_full'] = matchup.title_full()

    return result
@require_GET
def index_endpoint(request):
    fightEventDataState = FightEventDataState.objects.select_for_update().first()

    global WorkerThread
    if WorkerThread == None and fightEventDataState.updating:
        #invalid state start worker 
        WorkerThread = Thread(target=WorkerThreadControlFunction)
        WorkerThread.start()
    #in an invalid state
    if fightEventDataState.updating or fightEventDataState.staleOrEmpty:
        return JsonResponse({'available':False,"message":'currently updating'})
    
    nextEvent = FightEvent.objects.filter(date__gte=datetime.today().date()).order_by('date').first()
    prelims = list(map(lambda x:matchupDictWithName(x),MatchUp.objects.filter(event=nextEvent,isprelim=True)))
    mainCard = list(map(lambda x: matchupDictWithName(x),MatchUp.objects.filter(event=nextEvent,isprelim=False)))
    #split into main card and prelims
    
    context = {
        'available' : True,
        'message':'data is available',
        'event': model_to_dict(nextEvent),
        'mainCard': mainCard,
        'prelims':prelims,
    }

    return JsonResponse(context)

@require_GET
def index_alt(request):
    #purpose of index
    global WorkerThread
    fightEventDataState = FightEventDataState.objects.select_for_update().first()
    
    #event is stale if the latest event has a date before today
    today = datetime.today().date()
    nextEvent = FightEvent.objects.filter(date__gte=today).order_by('date').first()
    if nextEvent == None:
        fightEventDataState.staleOrEmpty = True
        fightEventDataState.save()

    if fightEventDataState.staleOrEmpty:
        print('EVENT IS STALE OR EMPTY')
        #compare current date and next event date
        fightEventDataState.updating=True
        if WorkerThread == None or not WorkerThread.is_alive():
            WorkerThread = Thread(target=WorkerThreadControlFunction)
            WorkerThread.start()
            #create new
        else:
            print('Currently updating from site.....')
        fightEventDataState.save()
    else:
        nextEvent = FightEvent.objects.filter(date__gte=today).order_by('date').first()
    #show next upcoming fight event
    # nextEvent = FightEvent.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
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
    
    print('event ==> ',nextEvent)
    context = {
        'event': nextEvent,
        'matchupsList': [mainCard,prelims],
    }

    return render(request, "fightEvaluator/index3.html",context)

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

    return render(request, "fightEvaluator/index3.html",context)

@require_GET
def events(request):
    #return a list of all events sorted by date
    events = FightEvent.objects.all().order_by('date').reverse()
    events_by_month = {}
    for event in events:
        month_year = event.date.strftime("%B %Y")
        if month_year not in events_by_month:
            events_by_month[month_year] = []
        events_by_month[month_year].append(event)
    return render(request,"fightEvaluator/events.html",{'events':events,'events_by_month':events_by_month})

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


def verifyPrediction(matchups):
    for matchup in matchups:
        prediction = Prediction.objects.filter(matchup=matchup).first()
        if prediction:
            outcome = matchup.outcome
            #if prediction has a fighter then it is a winner determination
            prediction.isCorrect = False
            match prediction.prediction.event:
                case Event.DOES_NOT_GO_THE_DISTANCE:
                    # print("")
                    #fights end method always decision if method == 'decision'
                    prediction.isCorrect = outcome.method != FightOutcome.Outcomes.DECISION
                case Event.ROUNDS_GEQ_ONE_AND_HALF:
                    if outcome.final_round > 2:
                        prediction.isCorrect = True
                    elif outcome.final_round == 2:
                        #time is str
                        #int:int
                        seconds = 30#
                        _,actual_seconds = outcome.time.split(":")
                        #if at least 30 seconds into the second minute for this event 
                        #then true else False
                        prediction.isCorrect = seconds >= actual_seconds
                case Event.WIN:
                    if outcome.winner != None and prediction.prediction.fighter == outcome.winner:
                        prediction.isCorrect = True

            prediction.save()

@require_GET
def getFightEventResults2(request,eventId):
    fightEvent = get_object_or_404(FightEvent,id=eventId)
    #do not try and get event results if the event is in the future
    #or if the it is not the atleast 2:00 am the day after the event
    if fightEvent.date > datetime.date.today() or datetime.datetime.now().hour < 2:
        return JsonResponse({'fightOutcomes':[],'error':'Results not available yet'})
    matchups = MatchUp.objects.filter(event=fightEvent)

    matchupResults = {}
    fightOutcomes = []
    if not fightEvent.hasResults:
        matchupResults = scraper.getFightEventResults2(fightEvent.link)
        nameMatchUpMap = {}
        for m in matchups:
            if m.fighter_a.name_unmod not in nameMatchUpMap:
                nameMatchUpMap[m.fighter_a.name_unmod] = m
                nameMatchUpMap[m.fighter_b.name_unmod] = m
        for mr in matchupResults:
            #find corresponding matchup from matchups
            fighters = mr['fighters']
            method = mr['method']
            final_round = mr['final_round']
            time = mr['time']

            matchup = None
            fa,fb = fighters
            if fa['name'] in nameMatchUpMap:
                matchup = nameMatchUpMap[fa['name']]
            elif fb['name'] in nameMatchUpMap:
                matchup = nameMatchUpMap[fb['name']]
            else:
                continue#skip this fight outcome
            #replace spaces with underscores
            method = method.replace(" ","_")
            matchup.outcome = FightOutcome()
            matchup.outcome.method = FightOutcome.Outcomes[method.upper()]
            matchup.outcome.time = time
            matchup.outcome.final_round = int(final_round)
            

            winnerName = None
            winner = None
            if fa['isWinner'] == True:
                winnerName = fa['name']
            elif fb['isWinner'] == True:
                winnerName = fb['name']
            
            if winnerName:
                winner = matchup.fighter_a
                if winnerName != matchup.fighter_a.name_unmod:
                    winner = matchup.fighter_b
            
            matchup.outcome.winner = winner
            matchup.outcome.save()
            matchup.save()
            fightOutcomes.append(model_to_dict(matchup.outcome))
        fightEvent.hasResults = True
        fightEvent.save()
    else:
        for m in matchups:
            fightOutcomes.append(model_to_dict(m.outcome))
    verifyPrediction(matchups)
    return JsonResponse({'puta':'madre'})
    

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
    