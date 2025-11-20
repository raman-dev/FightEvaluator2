from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page

from django.shortcuts import render,get_object_or_404,redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse

from django.views.generic import ListView,DetailView
from django.utils.decorators import method_decorator

from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Q


from ..models import Fighter,FightEvent,MatchUp,FightOutcome,Prediction,Event,FightEventDataState,EventStat
from ..forms import FightEventForm,MatchUpFormMF
from .prediction import calculate_stats

import json
import datetime
import re

from .. import scraper

from ..scraper import eventLinkParse,EVENTS_URL2
from ..scraper2 import scrapeMatchups

from ..scraper3 import printProcessInfo
from threading import Thread
import multiprocessing
from datetime import datetime
import concurrent
# from ..scraper import getUpcomingFightEvent
import scrapy
from scrapy.crawler import CrawlerProcess

WorkerThread = None
globalCounter = 0

from ..scrapy_server.commands import ServerCommands
from ..scrapy_server import scraper_client


scrapyThread = None
def scrapyThreadTestEndpoint(request):
    global scrapyThread
    if scrapyThread == None or not scrapyThread.is_alive():
        scrapyThread = Thread(target=ScrapyControlThreadFunction)
        scrapyThread.start()
        return JsonResponse({"state":"scrapy thread started"})
    return JsonResponse({"state":"scrapy thread running"})
#thread launches scrapy process
#and waits for it to complete
def ScrapyControlThreadFunction2():
    """
        start a client 
            tell the server what to do
    """
    with scraper_client.Client() as client:
        # client.send_command(ServerCommands.FETCH_EVENT_LATEST)
        
        pass
    

def ScrapyControlThreadFunction():
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
    """
    # with transaction.atomic():
    """
        **NOTE**
        CANNOT USE ProcessPoolExecutor since it may reuse an existing 
        process in the pool and scrapy does not allow the underlying
        twisted.reactor to be restarted once completed in the same process

        MUST CREATE A NEW PROCESS FOR EACH TIME I WANT TO USE SCRAPY
    """
    #get event
    p = multiprocessing.Process(
        target=printProcessInfo,
        kwargs={'sleep':2},
        daemon=True
    )
    p.start()
    p.join()
    # q = multiprocessing.Queue()
    # launchScrapyProcess(FightEventSpiderProcess,kwargs={'q':q})

    # eventResultList = []
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     eventResultFuture = executor.submit(startCrawlerProcess,EventLinkSpider)
    #     eventResultList = eventResultFuture.result()
    # eventDataResultList = q.get()#wait for a result
    # fightEventData = eventResultList[0]

    # # launchScrapyProcess(MatchUpSpiderProcess,kwargs={'eventLink':fightEventData['link'],'q':q})
    # # matchupsDataResultList = q.get()#wait for a result
    # matchupsResultList = []
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     MatchUpSpider.start_urls.append(fightEventData['link'])
    #     matchupResultFuture = executor.submit(startCrawlerProcess,MatchUpSpider)
    #     matchupsResultList = matchupResultFuture.result()
    # matchupsData = matchupsResultList[0]

    # fightEventData['title'] = matchupsData['title']
    # matchups = matchupsData['matchups']
    #matchups returned in this format
    """
        fighters_raw
            0 
                name
                link
            1
                name 
                link
        weight_class
        rounds
        isprelim

        matchup construction from raw data

        matchupRaw
            isprelim
            rounds
            weight_class
        
            fighter_a:obj or None if missing
            fighter_b:obj or None if missing

            fighter_a_link: str
            fighter_b_link: str
        matchupFighter404Queue
            matchupRawIndex,fighter_a,link
            matchupRawIndex,fighter_b,link
            ...
        for each matchup item
            check if db has each fighter
            if fighter_a and fighter_b in db
            we can construct a matchup

            if fighter_a not in db


    """
    # matchupsRaw = []
    # matchupFighter404Q = []
    # for i,m in enumerate(matchups):
    #     #create index key from name
    #     currMatchup = { 'isprelim':m['isprelim'], 'rounds':m['rounds'],'weight_class':m['weight_class']}
    #     for j,fighterData in enumerate(m['fighters_raw']):
    #         name,link = fighterData.values()
    #         names = [x.lower() for x in name.split(' ')]
    #         name_index = "-".join(names)
    #         first_name = names[0]
    #         last_name = ""
    #         if len(names) > 1:
    #             last_name = names[-1]

    #         #try name index
    #         fighterObj = Fighter.objects.filter(name_index=name_index).first()
    #         if not fighterObj:
    #             #try a first name last name query
    #             first_name_and_last_name_contains = Q(first_name=first_name) & Q(last_name__contains=last_name)
    #             fighterObj = Fighter.objects.filter(first_name_and_last_name_contains).first()
    #         key  = 'fighter_a' if i == 0 else 'fighter_b'
    #         currMatchup[key] = fighterObj
    #         if fighterObj == None:
    #             currMatchup[key + '_link'] = link

    #     if currMatchup['fighter_a'] == None:
    #         matchupFighter404Q.append(currMatchup['fighter_a_link'])
    #     if currMatchup['fighter_b'] == None:
    #         matchupFighter404Q.append(currMatchup['fighter_b_link'])
        
    #     matchupsRaw.append(currMatchup)
    # for m in matchupsRaw:
    #     print(m)
    # for m in matchupFighter404Q:
    #     print(m)
    # if len(matchupFighter404Q) != 0:
    #     pass
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     #scrape tapology website for upcoming event
    #     #return the link data for the event
    #     eventFetchFuture = executor.submit(startCrawlerProcess,(EventLinkSpider))
    #     eventDataResultList = eventFetchFuture.result()#returns a list of results
    #     #now visit the event link and grab all matchup data
    #     #validate with 
    #     fightEventData = eventDataResultList[0]
        
    #     MatchUpSpider.start_urls.append(fightEventData['link'])
    #     matchupsDataFuture = executor.submit(startCrawlerProcess,(MatchUpSpider))
    #     matchupsDataResultList = matchupsDataFuture.result()
        
    #     matchupsData = matchupsDataResultList[0]

    #     fightEventData['title'] = matchupsData['title']
    # pass

            
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
            if matchupForm.is_valid():#save all that are valid 
                # return JsonResponse({'MatchUpFormMF':'FUCKED','error':matchupForm.errors})
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
def index(request):
    return redirect("/136")
    #purpose of index
    global WorkerThread
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
    fightEvent = get_object_or_404(FightEvent,id=eventId)
    #do not try and get event results if the event is in the future
    #or if the it is not the atleast 2:00 am the day after the event
    # if fightEvent.date > datetime.today().date() or datetime.now().hour < 2:
    #     return JsonResponse({'fightOutcomes':[],'error':'Results not available yet'})
    matchups = MatchUp.objects.filter(event=fightEvent)

    matchupResults = {}
    fightOutcomes = []
    if not fightEvent.hasResults:
        matchupResults = scraper.getFightEventResults2(fightEvent.link)
        print(matchupResults)
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
            fightOutcomes.append(model_to_dict(matchup.outcome))
        fightEvent.hasResults = True
        fightEvent.save()
    else:
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