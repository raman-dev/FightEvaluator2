from fightEvaluator.models import MatchUpOutcome,Likelihood,Event,EventLikelihood


def o2el():
    #read in the outcomes from the database
    outcomes = MatchUpOutcome.objects.all()
    for outcome in outcomes:
        eventLikelihood = EventLikelihood()
        eventLikelihood.matchup = outcome.matchup
        eventLikelihood.justification = outcome.justification
        eventLikelihood.likelihood = outcome.likelihood

        if outcome.fighter != None:
            eventLikelihood.event = Event.WIN
        # else:
        for event in Event:
            # print(event.name,event.value)
            if event.value == outcome.outcome:
                eventLikelihood.event = event
                eventLikelihood.event_name = event.name
        
        if outcome.fighter != None:
            eventLikelihood.fighter = outcome.fighter
        eventLikelihood.save()
        # break
        

o2el()