from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.forms.models import model_to_dict

from django.http import JsonResponse
from ..models import *

from rich.pretty import pprint 
import time
from datetime import datetime

# @cache_page(10)
def cache_test(request):
    print(request.headers)
    # print(request.GET)
    key = "cache-test-key"
    value = request.GET.get("value")
    print(key,value)
    if cache.get(key) != None:
        return JsonResponse({"from cache":True,key:value})
    else:
        cache.set(key,value,timeout=60)
    return JsonResponse({key:value})

def cacheTest(request):
    start = time.time()
    events = []
    eventQuerySet = FightEvent.objects.all()

    currentYear = datetime.today().year
    key = f'all-events-{currentYear}'
    cached = cache.get(key)
    if cached != None:
        end = time.time()
        elapsed = f'{end - start:.6f}'
        return JsonResponse({'cached':True,'timeTaken':elapsed,'events':cached})
    else:
        for year in range(2023,currentYear + 1):
            yearSet = eventQuerySet.filter(date__year=year)
            months = []
            for month in range(0,13):
                t = [model_to_dict(x) for x in yearSet.filter(date__month=month)]
                if len(t) ==0:
                    continue
                t.sort(key=lambda x: x['date'],reverse=True)
                mes = MonthlyEventStats.objects.filter(year=year,month=month)
                mesDict = {}
                if mes.exists():
                    mesDict = model_to_dict(mes[0]) | {'accuracy':mes[0].accuracy}
                
                months.append ({
                    'month':month,
                    'events':t,
                    'monthlyStats': mesDict
                })
            months.sort(key=lambda x:x['month'],reverse=True)
            events.append({
                'year':year,
                'months': months
            })
    """

        events:[
            {
                year: y
                months:  [
                    {month: i, events: events.sorted.reverse}
            ]},...
        ]

    """
    events.sort(key=lambda x :x['year'],reverse=True)
    end = time.time()
    elapsed = f'{end - start:.6f}'
    cache.set(key,events,timeout=60)
    return JsonResponse({'cached':False,'timeTaken':elapsed,'events':events})