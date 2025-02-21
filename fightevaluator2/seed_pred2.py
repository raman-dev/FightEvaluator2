from fightEvaluator.models import EventLikelihood,Prediction,Pick,Prediction2

def create_pred2():
    #grab all prediction objects
    for e in EventLikelihood.objects.all():
        p = Prediction2(
            matchup=e.matchup,
            event=e.event,
            eventType=e.eventType,
            likelihood=e.likelihood,
            justification=e.justification,
            fighter=e.fighter
        )
        p.save()
        

def create_picks():
    for p in  Prediction.objects.all():
            #copy p.prediction.event to p.event
        pred2 = Prediction2.objects.get(matchup=p.matchup,event=p.prediction.event,fighter=p.prediction.fighter)
        pick = Pick(
            matchup=p.matchup,
            prediction=pred2,
            isGamble=p.isGamble,
            isCorrect=p.isCorrect
        )
        pick.save()
