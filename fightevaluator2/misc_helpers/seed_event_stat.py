from fightEvaluator.models import FightEvent,EventStat,MonthlyEventStats,Prediction,MatchUp
from django.db.models import Avg,Count,Q
"""
    create eventstat rows
        for every event 

        store number of predictions
        number of correct predictions

"""

def updateEventStat(eventStat: EventStat,prediction: Prediction):
    eventStat.predictions += 1
    if prediction.isCorrect:
        eventStat.correct += 1
    eventStat.save()


def run():
    preds = Prediction.objects.all()
    #pred -> matchup -> event
    #update(eventStat,pred)
    #update(monthlyEventStat,eventStat)
    eventStatCache = {}
    monthStatCache = {}
    for p in preds:
        # print(p)
        event = p.matchup.event
        eventStat = None
        if event.id not in eventStatCache:
            eventStat = EventStat(event=event,predictions=0,correct=0)
            eventStatCache[event.id] = eventStat
        else:
            eventStat = eventStatCache[event.id]
            # eventStat.refresh_from_db()
        updateEventStat(eventStat,p)
        
        year,month = event.date.year,event.date.month
        # print(year,month)
        mes = None
        if year not in monthStatCache:
            monthStatCache[year] = {}
        if month not in monthStatCache[year]:
            mes = MonthlyEventStats(year=year,month=month,events=0,predictions=0,correct=0)
            monthStatCache[year][month] = mes
        else:
            mes = monthStatCache[year][month]
            # mes.refresh_from_db()
        
        mes.predictions += 1
        if p.isCorrect == True:
            mes.correct += 1
        mes.save()
    events = FightEvent.objects.all()
    for year in monthStatCache.keys():
        for month in monthStatCache[year].keys():
            result = events.aggregate(numEvents=Count('id',filter=Q(date__year=year,date__month=month)))
            monthStatCache[year][month].events = result['numEvents']
            monthStatCache[year][month].save()
    print(monthStatCache)


run()
        


