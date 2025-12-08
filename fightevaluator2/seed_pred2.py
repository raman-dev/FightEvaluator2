from fightEvaluator.models import EventLikelihood,Prediction,Pick,Prediction2
from django.db import transaction

def create_pred2():
    
    print("Creating Prediction2 objects from Prediction/EventLikelihood")
    with transaction.atomic():
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
            print(p)
            p.save()
        

def create_picks():
    print("Creating Pick objects from Prediction objects")
    with transaction.atomic():
        for p in Prediction.objects.all():
                #copy p.prediction.event to p.event
            pred2 = Prediction2.objects.get(matchup=p.matchup,event=p.prediction.event,fighter=p.prediction.fighter)
            pick = Pick(
                event=pred2.event,
                matchup=p.matchup,
                prediction=pred2,
                isGamble=p.isGamble,
                isCorrect=p.isCorrect
            )
            pick.save()

# if __name__=="__main__":
#     create_pred2()
#     create_picks()

def run():
    create_pred2()
    create_picks()
