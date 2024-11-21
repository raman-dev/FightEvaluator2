from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Count, Q
from .draft_kings_scraper import draftkings_scraper

from rich import print as rprint

def toMultiplier(odd):
    if odd > 0:
        return round(1 + odd / 100, 2)
    return round(1 + 100 / abs(odd), 2)


@require_GET
def profit_data(request):
     #check if data available
     #if available return data
     #else return empty list or flag
     return JsonResponse({'fuck':'you'})

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
    if draftkings_scraper.isStaleOrEmpty():
        #do work
        rprint('Do work in thread and return page without data')
        #inside template check if empty length of data
        #include polling script if empty
        # return render(request, "fightEvaluator/profit.html", {"oddsList": oddsListMap})
    else:
        #query from file
        rprint('Available in file')
        oddsList = draftkings_scraper.run()
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
