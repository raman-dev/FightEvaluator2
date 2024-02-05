from fightEvaluator.models import MatchUpOutcome,Likelihood,Event,EventLikelihood


def o2el():
    #read in the outcomes from the database
    outcomes = MatchUpOutcome.objects.all()
    for outcome in outcomes:
        print(outcome.likelihood,outcome.matchup)
        print(Likelihood.choices)
        eventLikelihood = {}
        for choice in Likelihood.choices:
            if choice[0] == outcome.likelihood:
                eventLikelihood['likelihood'] = choice[0]
                break
        

o2el()