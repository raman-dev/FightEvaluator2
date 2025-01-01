from fightEvaluator.models import FightEvent,Fighter,MatchUp,MatchUp2

def create_matchup2_records():
    for old_matchup in MatchUp.objects.all():
        
        new_matchup = MatchUp2(
            event=old_matchup.event,
            fighter_a=old_matchup.fighter_a,
            fighter_b=old_matchup.fighter_b,
            weight_class=old_matchup.weight_class,
            rounds = old_matchup.rounds,
        )

        if old_matchup.isprelim != None:
            new_matchup.is_prelim = old_matchup.isprelim
        if old_matchup.inWatchList != None:
            new_matchup.in_watchlist = old_matchup.inWatchList
        
        if old_matchup.analysisComplete != None:
            new_matchup.analysis_complete = old_matchup.analysisComplete
        
        new_matchup.save()
