from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Count,Q
from .draft_kings_scraper import draftkings_scraper

def toMultiplier(odd):
        if odd > 0:
                return round(1 + odd/100,2)
        return round(1 + 100/abs(odd),2)

@require_GET
def profit_calculator(request):
        oddsList = draftkings_scraper.run()
        oddsListMap = []
        for fa,fb,oa,ob in oddsList:
                oddsListMap.append({
                        'fighter_a':fa,
                        'fighter_b':fb,
                        'mult_a':toMultiplier(oa),
                        'mult_b':toMultiplier(ob),
                        'odds_a':oa,
                        'odds_b':ob
                        })
        return render(request, "fightEvaluator/profit.html",{'oddsList':oddsListMap})
