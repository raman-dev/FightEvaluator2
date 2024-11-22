from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Count, Q
from .draft_kings_scraper import draftkings_scraper

from ..models import OddsDataState
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
        oddsList = draftkings_scraper.getOddsFromFile()  # query from file
        for fa, fb, oa, ob in oddsList:
            oddsListMap.append(
                {
                    "fighter_a": fa,
                    "fighter_b": fb,
                    "mult_a": toMultiplier(oa),
                    "mult_b": toMultiplier(ob),
                    "odds_a": oa,
                    "odds_b": ob,
                }
            )
        return JsonResponse({"available":True,'oddsList':oddsListMap})
    # if not updating then check if
    # else return empty list or flag
    return JsonResponse({"available": False})


def OddsWorkerThreadControlFunction():
    print('WorkerThread Fetching from Site....')
    draftkings_scraper.fetchFromSite()
    # no longer stale or empty
    oddsDataState = OddsDataState.objects.select_for_update().first()
    oddsDataState.updating = False
    oddsDataState.staleOrEmpty = False
    oddsDataState.date = datetime.today().date()  # write today's date
    oddsDataState.save()


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
            WorkerThread = Thread(target=OddsWorkerThreadControlFunction)
            WorkerThread.start()
    else:
        if WorkerThread != None and WorkerThread.is_alive():
            WorkerThread.join()
        # query from file
        rprint("Available in file")
        oddsList = draftkings_scraper.getOddsFromFile()  # query from file
        for fa, fb, oa, ob in oddsList:
            oddsListMap.append(
                {
                    "fighter_a": fa,
                    "fighter_b": fb,
                    "mult_a": toMultiplier(oa),
                    "mult_b": toMultiplier(ob),
                    "odds_a": oa,
                    "odds_b": ob,
                }
            )
    return render(request, "fightEvaluator/profit.html", {"oddsList": oddsListMap})
