from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page

from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse

from django.views.generic import ListView,DetailView
from django.utils.decorators import method_decorator

from django.db import transaction,OperationalError
from django.db.models import Q

from ..models import *
from ..forms import FightEventForm,MatchUpFormMF,FighterForm
from .prediction import calculate_stats

import time
import datetime

from .. import scraper

from threading import Thread
from datetime import datetime
# from ..scraper import getUpcomingFightEvent

WorkerThread = None
globalCounter = 0
MAX_RETRIES = 15
RETRY_DELAY_S = 3

from ..scrapy_server.commands import ServerCommands
from ..scrapy_server import scraper_client

from rich import print as rprint

PORT = 42069
scrapyFightEventThread = None
scrapyEventResultsThread = None

#thread launches scrapy process
#and waits for it to complete
def ScrapyFightEventControlFunction():
    #this function is launched when the newest event has not been fetched or created
    """
        do what here
        launch a scrapy process with a pool
            scrapy process
                query fight event for page source
                break into matchups with fighter links and names
                return to thread
            if all fighters of matchups in db
                save all matchups with corresponding fighter objects
            else:
                queue list of unknown fighters
                launch scrapy process to fetch fighter data
                    return fighter info to thread
                create fighter objects
                save all matchups with corresponding fighter objects  

            complete
        assume runs uninterrupted

        ScraperClient extends Client
            
            getNextEvent() -> dict: 

            getFighter(link: str)

    """
    # with transaction.atomic():
    """
        **NOTE**
        CANNOT USE ProcessPoolExecutor since it may reuse an existing 
        process in the pool and scrapy does not allow the underlying
        twisted.reactor to be restarted once completed in the same process

        MUST CREATE A NEW PROCESS FOR EACH TIME I WANT TO USE SCRAPY
    """
    # attempts = 0
    with scraper_client.ZmqReqClient(serverPort=PORT) as client:
        #response = fetcher.nextEvent()
        response = client.sendCommandRetryLoop(command=ServerCommands.FETCH_EVENT_LATEST)
        fighterData = response['data']
        
        fightEventData = fighterData['event']
        matchupsRaw = fighterData['matchups']
        matchups = []
        rprint(matchupsRaw)
        
        fightEventForm = FightEventForm(fightEventData)
        fightEvent = None
        if fightEventForm.is_valid():
            # fightEvent = fightEventForm.save()
            rprint("[bold cyan]Event Valid[/bold cyan]")
            
        for matchupData in matchupsRaw:
            rprint("")
            matchup = {
                'weight_class':scraper.poundsToWeightClass(matchupData['weight_class']),
                'rounds':matchupData['rounds'],
                'isprelim':matchupData['isprelim']
            }
            for i,fighter in enumerate(matchupData['fighters_raw']):
                #check if fighter is in database
                name = fighter['name']
                names = list(map(lambda x: x.lower(), name.split(' ')))
                name_index = "-".join(names)#search using this
                first_name = names[0]#try only first name
                last_name = names[-1]#last name may include middle name
                if len(name) > 1:
                    last_name = " ".join(names[1:])

                rprint("\t",first_name,last_name,name_index)

                first_name_and_last_name_contains=Q(first_name=first_name) & Q(last_name__contains=last_name)
                query_a = first_name_and_last_name_contains
                fighterObj = Fighter.objects.filter(name_index=name_index).first()
                if not fighterObj:            
                    fighterObj = Fighter.objects.filter(query_a).first()
                    if fighterObj == None:
                        rprint("No fighter object found")
                        # response = fetcher.fetchFighter(link=fighter['link'])
                        response = client.sendCommandRetryLoop(ServerCommands.FETCH_FIGHTER,data={'link':fighter['link']})
                        if response:
                            fighterData = response['data']
                            rprint(fighterData)
                            
                            fighterData['data_api_link'] = fighter['link']
                            
                            if fighterData['date_of_birth'] == 'N/A':
                                fighterData['date_of_birth'] = None#datetime.strptime("2001-01-01","%Y-%m-%d").date()
                            
                            weight_class = WeightClass[fighterData['weight_class']]
                            fighterData['weight_class'] = weight_class
                            fighterForm = FighterForm(fighterData)#validate fighter data
                            
                            if fighterForm.is_valid():
                                fighterObj = fighterForm.save()

                                rprint('Valid fighter',fighterObj)
                                assessment = Assessment(fighter=fighterObj)
                                assessment.save()
                                
                                fighterObj.assessment = assessment
                                # fighterObj.save()
                            else:
                                rprint(fighterForm.errors)
                                break
                        time.sleep(10)#need to sleep before fetching again if we have to
                
                if i == 0:
                    matchup['fighter_a'] = fighterObj
                else:
                    matchup['fighter_b'] = fighterObj
            matchups.append(matchup) 
            rprint(matchup)
        
        fightEvent = fightEventForm.save()
        for m in matchups:
            m['event'] = fightEvent
            m['scheduled'] = fightEvent.date
            mf = MatchUpFormMF(m)
            if mf.is_valid():
                mf.save()
        """     
                event:
                link 
                date
                title
            matchups: 
                0
                    fighters_raw
                        0: name 
                            link
                        1: name
                            link
                    weight_class
                    rounds
                    isprelim

                1   fighters_raw
                        0: name
                            link
                        1: name
                            link
                    weight_class
                    rounds
                    isprelim
                {
        """ 

    fightEventDataState = FightEventDataState.objects.select_for_update().first()
    fightEventDataState.staleOrEmpty = False
    fightEventDataState.updating = False
    fightEventDataState.date = datetime.today().date()
    fightEventDataState.save()

def ScrapyEventResultsControlFunction(eventId: int):
    with transaction.atomic():
        fightEvent = FightEvent.objects.select_for_update().filter(id=eventId).first()
        # response = None python3 only has function scope inner and outer and global scope
        #block scoping isn't a thing
        #however don't do this kind of bad practice, too implicit to the language 
        response = None
        with scraper_client.ZmqReqClient(serverPort=PORT) as client:
            response = client.sendCommandRetryLoop(ServerCommands.FETCH_EVENT_RESULTS,{'link':fightEvent.link})
        if response:
            matchupResults = response['data']
            print(matchupResults)
            matchups = MatchUp.objects.select_for_update().filter(event=fightEvent)
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
                
                #update winner/loser win/loss count
                if winnerName:
                    #fighter_a is winner
                    winner = matchup.fighter_a
                    loser = matchup.fighter_b
                    #fighter_b is winner
                    if winnerName != matchup.fighter_a.name_unmod:
                        winner = matchup.fighter_b
                        loser = matchup.fighter_a
                    
                    winner.wins = winner.wins + 1
                    loser.losses = loser.losses + 1
                    
                    winner.save()
                    loser.save()

                matchup.outcome.winner = winner
                matchup.outcome.save()
                matchup.save()
                # fightOutcomes.append(model_to_dict(matchup.outcome))
            fightEvent.hasResults = True
            fightEvent.save()
    
"""
     client          django-server                            scraper-server
        get index------>
                        check has event
                        data
                <-----data available  
                        data unavailable
                        if isUpdating
                <-----currently updating
                        if not updating
                        ask scraper-server
                        for event data
                           if event data unavailable
                           determine why?
                              scraper-server processing?
                              if processing
                <---------------currently updating
                              if not processing
                               start 
                               scraper-server update
                                 process--------------------->
                                
                                                  start-----> start scraper process for next event data
                                                              write to json file when complete
                                                              return response from scraper-server
                                <------------------------------event data                                                     
                        when data available
                         process json data 
                         create fight event models 
                         for every matchup
                            check if fighter in db 
                            if not in db
                                add to fighter fetch queue
                        if fighter fetch queue not empty
                            send fetch fighter
                              request to scraper-server-------------------->
                                                                start-----> start scraper process for fighter data
                                                                            write to json file when complete
                                                                            return response from scraper-server
                                    <------------------------------fighter data
                            create fighter models for fetched fighters
                        create matchup models for every matchup
                        mark event data state as not stale/updating
"""

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

    global scrapyFightEventThread
    if scrapyFightEventThread == None and fightEventDataState.updating:
        #invalid state start worker 
        scrapyFightEventThread = Thread(target=ScrapyFightEventControlFunction)
        scrapyFightEventThread.start()
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
def index(request):
    #purpose of index
    global scrapyFightEventThread
    fightEventDataState = FightEventDataState.objects.select_for_update().first()
    
    #event is stale if the latest event has a date before today
    today = datetime.today().date()
    nextEvent = FightEvent.objects.filter(date__gte=today).order_by('date').first()
    if nextEvent == None:
        fightEventDataState.staleOrEmpty = True
        fightEventDataState.save()

    if fightEventDataState.staleOrEmpty == True:
        print('EVENT IS STALE OR EMPTY')
        #compare current date and next event date
        fightEventDataState.updating=True
        if scrapyFightEventThread == None or not scrapyFightEventThread.is_alive():
            scrapyFightEventThread = Thread(target=ScrapyFightEventControlFunction)
            scrapyFightEventThread.start()
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

    return render(request, "fightEvaluator/index.html",context)

@method_decorator(cache_page(60 * 2), name="dispatch")
class FightEventListView(ListView):
    model = FightEvent
    #we need to return a map that has grouped the events by month 
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        events = context['fightevent_list']
        events_by_month = {}
        for event in events:
            month_year = event.date.strftime("%B %Y")
            if month_year not in events_by_month:
                events_by_month[month_year] = []
            events_by_month[month_year].append(event)
        context['events_by_month'] = events_by_month
        context.pop('fightevent_list')
        return context

class FightEventDetailView(DetailView):
    model = FightEvent

    def get_object(self, queryset = None):
        # print('PK_URL_KWARG',self.pk_url_kwarg)
        # print(type(self.kwargs))
        if self.pk_url_kwarg not in self.kwargs: 
            pk = FightEvent.objects.all().first().pk
            self.kwargs[self.pk_url_kwarg] = pk
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        mainCard = MatchUp.objects.filter(event=event,isprelim=False)
        prelims = MatchUp.objects.filter(event=event,isprelim=True)
        context['matchupsList'] = [mainCard,prelims] #collected into 1 list to reduce
        #html repetition in template
        return context

def verifyPrediction(matchups):
    m  = matchups[0]
    esQuerySet = EventStat.objects.filter(event=m.event)
    es = None
    if not esQuerySet.exists():
        es = EventStat(event=m.event,predictions=0,correct=0)
    else:
        es = esQuerySet[0]
    es.correct = 0
    es.predictions = 0
    for matchup in matchups:
        prediction = Prediction.objects.filter(matchup=matchup).first()
        if prediction:
            
            es.predictions += 1
            outcome = matchup.outcome
            print(outcome,'predictions => ',prediction)
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
                        minutes,actual_seconds = outcome.time.split(":")
                        #if at least 30 seconds into the second minute for this event 
                        #then true else False
                        prediction.isCorrect = int(minutes) > 2 or (int(minutes) == 2 and int(actual_seconds) >= seconds)

                case Event.WIN:
                    if outcome.winner != None and prediction.prediction.fighter == outcome.winner:
                        prediction.isCorrect = True

            prediction.save()
            """
                for this event 
                    grab eventStat object if doesn't exist

            """

            if prediction.isCorrect:
                es.correct += 1
    es.save()
    calculate_stats()

def update_stats(request):
    calculate_stats()
    return JsonResponse({"ok":"true"})

@require_GET
def getFightEventResults2(request,eventId):
    # fightEvent = get_object_or_404(FightEvent,id=eventId)
    if not FightEvent.objects.filter(id=eventId).exists():
        return JsonResponse({"Error":"Event does not exist"})
    #do not try and get event results if the event is in the future
    #or if the it is not the atleast 2:00 am the day after the event
    fightEvent = FightEvent.objects.filter(pk=eventId).first()
    
    if fightEvent.date > datetime.today().date() or datetime.now().hour < 2:
        return JsonResponse({'fightOutcomes':[],'error':'Results not available yet'})
    if not fightEvent.hasResults:#reading concurrently is always valid
        #until the concurrent write has happened the old value will always be available
        global scrapyFightEventThread
        if scrapyEventResultsThread != None and scrapyEventResultsThread.is_alive():
            return JsonResponse({"message":"Currently fetching results..."})

        #scrapyEventResultsThread is none or not alive
        #invalid state start worker 
        scrapyFightEventThread = Thread(target=ScrapyEventResultsControlFunction,args=[],kwargs={'eventId':fightEvent.id})
        scrapyFightEventThread.start()
        return JsonResponse({"message":"Will now start fetching results..."})
      
    else:
        fightOutcomes = []
        matchups = MatchUp.objects.filter(event=fightEvent)
        for m in matchups:
            if m.outcome != None:
                fightOutcomes.append(model_to_dict(m.outcome))
        verifyPrediction(matchups)
        return JsonResponse({'outcomes':fightOutcomes})
    
#maybe asynchronous in the future evaluate
#fetch results from web if not already in database
@cache_page(60 * 2)
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


@require_GET
def lockedRowAccess(request):
    """
    
        concurrent reading is always safe
        when writing
        wrap in transaction.atomic()
            then use select for update
    
    """
    """
    Will throw an OperationalError because the database is locked
    f = Fighter.objects.select_for_update().filter(id=1).first()
    f.losses += 1
    f.save()

    locking works with sqlite
    """
    with transaction.atomic():
        # f = Fighter.objects.select_for_update().filter(id=1).first()
        # f = Fighter.objects.select_for_update(nowait=True).filter(id=1).first()
        qset = Fighter.objects.select_for_update().filter(id=1)
        # if f != None:
        # f.losses += 1
        try: 
            # f.save()
            for f in qset:
                # f.losses += 1
                # f.save()
                rprint(f.wins)
            return JsonResponse({"msg":model_to_dict(f)})
        except OperationalError as e:
            rprint("Database is locked try again later")
            return JsonResponse({"msg":"Database is locked try again later"})
        # else:
        #     return JsonResponse({"msg":"Object is None"})

    return JsonResponse({"msg":"wtf!"})#unreachable

def lockRow(lockTime: int=30):
    with transaction.atomic():
        f = Fighter.objects.select_for_update().filter(id=1).first()
        rprint(model_to_dict(f))
        f.wins += 1
        f.save()
        time.sleep(lockTime)
        rprint("ROW_LOCK_THREAD_COMPLETE!")

@require_GET
def lockTestRow(request):
    #lock a row in a seperate thread
    lockTime = 45
    t = Thread(target=lockRow,args=[],kwargs={'lockTime':lockTime})
    t.start()

    return JsonResponse({"msg":f"Trying to lock fighter.1 for {lockTime}s"})


def polling_index(request):
    return render(request,"fightEvaluator/polling-index.html",{})

def polling_end(request):
    global globalCounter
    if globalCounter < 5:
        globalCounter += 1
        return render(request,"fightEvaluator/polling-wait.html",{})

    globalCounter = 0
    return render(request,"fightEvaluator/polling-result.html",{},status=286)

"""@require_GET
NOTE replaced with class based view
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

    return render(request, "fightEvaluator/index.html",context)

@require_GET
def events(request):
    #return a list of all events sorted by date
    events = FightEvent.objects.all()#.order_by('date').reverse()
    events_by_month = {}
    for event in events:
        month_year = event.date.strftime("%B %Y")
        if month_year not in events_by_month:
            events_by_month[month_year] = []
        events_by_month[month_year].append(event)
    return render(request,"fightEvaluator/events.html",{'events_by_month':events_by_month})
"""