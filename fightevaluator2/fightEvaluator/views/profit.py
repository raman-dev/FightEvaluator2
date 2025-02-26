from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Count, Q
# from .draft_kings_scraper import draftkings_scraper
from . import odds_scraper

from ..models import OddsDataState,Event,FightEvent,MatchUp,Prediction,EventLikelihood,Likelihood
from rich import print as rprint
from threading import Thread
from datetime import datetime

WorkerThread = None


def toMultiplier(odd):
    if odd > 0:
        return round(1 + odd / 100, 2)
    return round(1 + 100 / abs(odd), 2)


@require_GET
def get_odds(request):
    # check if data available
    # if available return data
    # check if updating
    oddsDataState = OddsDataState.objects.select_for_update().first()
    if oddsDataState.staleOrEmpty == False and oddsDataState.updating == False:
        oddsListMap = []
        oddsList = odds_scraper.getOddsFromFile()  # query from file
        for fa, fb, oa, ob in oddsList:
            oddsListMap.append(
                {
                    "fighter_a": fa,
                    "fighter_b": fb,
                    "mult_a": toMultiplier(oa),
                    "mult_b": toMultiplier(ob),
                    "odds_a": oa,
                    "odds_b": ob,
                    "xodds":{
                        "odds_a": oa,
                        "odds_b": ob,
                        "odds_rounds_ge_one_half": -1,
                        "odds_fight_does_not_go_the_distance": -1,
                    }
                }
            )
        return JsonResponse({"available":True,'oddsList':oddsListMap})
    # if not updating then check if
    # else return empty list or flag
    return JsonResponse({"available": False,'message':'updating odds.'})


def OddsWorkerThreadControlFunction(**kwargs):
    print(kwargs)
    event = kwargs['event']
    print('WorkerThread Fetching from Site....')
    odds_scraper.fetchFromSite(event.date)
    # no longer stale or empty
    oddsDataState = OddsDataState.objects.select_for_update().first()
    oddsDataState.updating = False
    oddsDataState.staleOrEmpty = False
    oddsDataState.date = datetime.today().date()  # write today's date
    oddsDataState.save()


@require_GET
def profit_index(request,eventId=-1):
    #for every matchup grab all predictions for 
    #3 events
    event = None
    if eventId == -1:
        event = FightEvent.objects.first()
    else:
        event = get_object_or_404(FightEvent,id=eventId)
    matchups = MatchUp.objects.filter(event=event)
    events = [Event.WIN,Event.ROUNDS_GEQ_ONE_AND_HALF,Event.DOES_NOT_GO_THE_DISTANCE]
    matchup_preds = []
    for m in matchups:
        #grab all predictions 
        preds = []
        empty_count = 0
        for e in events:
            
            result = EventLikelihood.objects.filter(matchup=m,event=e)
            if result.count() == 0:
                empty_count+=1
            if e == Event.WIN:
                #we want to first get fighter_a
                #then fighter_b
                if result.count() == 0:
                    #an unsaved model instance
                    preds.append(EventLikelihood.get_placeholder(m,e,m.fighter_a))
                    preds.append(EventLikelihood.get_placeholder(m,e,m.fighter_b))
                elif result.count() == 2:
                    preds.append(result.get(fighter=m.fighter_a))
                    preds.append(result.get(fighter=m.fighter_b))
                else:
                    #only 1 win predicted
                    print(result)
                    single_win_pred = result.first()
                    if single_win_pred.fighter == m.fighter_a:
                        preds.append(single_win_pred)
                        preds.append(EventLikelihood.get_placeholder(m,e,m.fighter_b))
                    else:
                        preds.append(EventLikelihood.get_placeholder(m,e,m.fighter_a))
                        preds.append(single_win_pred)
                        
            else:
                p = result.first()
                if p == None:
                    p = EventLikelihood.get_placeholder(m,e)
                preds.append(p)
        if empty_count < len(events):
            matchup_preds.append((m,preds))
    return render(request, 
                  template_name="fightEvaluator/profit_index.html", 
                  context={
                      "matchup_preds_list": matchup_preds,
                      "theads":["Win","Rounds >= 1.5","Does Not Go The Distance"],
                      })


@require_GET
def profit_calculator(request):
    """
    receive request
        check if upto date
            if upto date query file and get odds
            else:
               launch scraper on seperate thread
               return not upto date try again later

    """
    oddsListMap = []
    oddsDataState = OddsDataState.objects.select_for_update().first()
    today = datetime.today().date()
    event = FightEvent.objects.first()
    global WorkerThread

    # check if oddsDataState is stale or not
    if not oddsDataState.updating and (oddsDataState.date == None or oddsDataState.date != today):
        oddsDataState.staleOrEmpty = True

    if oddsDataState.staleOrEmpty:
        if not oddsDataState.updating:
            # do work
            oddsDataState.updating = True
            oddsDataState.save()
            rprint("Do work in thread and return page without data")

            # inside template include polling script
            # if WorkerThread == None or not WorkerThread.is_alive():#worker not running or
            WorkerThread = Thread(target=OddsWorkerThreadControlFunction,kwargs={'event':event})
            WorkerThread.start()
    else:
        if WorkerThread != None and WorkerThread.is_alive():
            WorkerThread.join()
        # query from file
        rprint("Available in file")
        oddsList = odds_scraper.getOddsFromFile()  # query from file
        for fa, fb, oa, ob in oddsList:
            oddsListMap.append(
                {
                    "fighter_a": fa,
                    "fighter_b": fb,
                    "mult_a": toMultiplier(oa),
                    "mult_b": toMultiplier(ob),
                    "odds_a": oa,
                    "odds_b": ob,
                    "xodds":{
                        "odds_a": oa,
                        "odds_b": ob,
                        "odds_rounds_ge_one_half": -1,
                        "odds_fight_does_not_go_the_distance": -1,
                    }
                }
            )
    return render(request, "fightEvaluator/profit.html", {"matchupOddsList": oddsListMap})
