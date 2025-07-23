from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse


from datetime import datetime
from ..models import FightEvent,MatchUp


@require_GET
def vueIndex(request):
    """
    Render the Vue.js index page.
    """
    return render(request, 'fightEvaluator/vue_index.html')

@require_GET
def vueFightEvent(request):
    #return the next fight event
    #get current day date
    current_date = datetime.now().date()
    #from FightEvent model, get the first event that is after or on the current date
    event = FightEvent.objects.filter(date__gte=current_date).order_by('date').first()
    if event:
        #convert the event to a dictionary
        event_dict = model_to_dict(event)
        #get matchups related to the event
        matchups = MatchUp.objects.filter(event=event)
        result = {
            'event': event_dict
        }
        #add fighter names to the matchups 
        mainCardJSON = []
        prelimJSON = []

        for isprelim_state in (True,False):
            matchups = MatchUp.objects.filter(event=event,isprelim=isprelim_state)
            for m in matchups:
                matchup_dict = model_to_dict(m)
                matchup_dict['fighter_a_name'] = m.fighter_a.name 
                matchup_dict['fighter_b_name'] = m.fighter_b.name 
                if isprelim_state:
                    prelimJSON.append(matchup_dict)
                else:
                    mainCardJSON.append(matchup_dict)

        result['mainCardMatchups'] = mainCardJSON
        result['prelimMatchups'] = prelimJSON
        return JsonResponse(result)
    return JsonResponse({'No Event Upcoming':None})