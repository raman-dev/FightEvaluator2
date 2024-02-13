from fightEvaluator.models import MatchUp,MatchUpPrediction,Prediction

#copy matchupPredictions to predictions
def copy():
    for mp in MatchUpPrediction.objects.all():
        p = Prediction()
        p.matchup = mp.matchup
        p.prediction = mp.prediction
        p.isGamble = mp.isGamble
        p.save()