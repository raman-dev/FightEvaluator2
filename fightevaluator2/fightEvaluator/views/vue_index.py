from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse


# from ..forms import PickForm
from datetime import datetime
from ..models import *
from ..forms import *
import json


@require_GET
def vueIndex(request):
    """
    Render the Vue.js index page.
    """
    return render(request, 'fightEvaluator/vue_index.html')

@require_GET
def get_event(request,eventId):
    resultSet = FightEvent.objects.filter(pk=eventId)
    if not resultSet:
        return JsonResponse({'No such event':None})
    event = resultSet[0]
    return aggregateAndParseEventMatchups(event)

@require_GET
def vueAllEvents(request):
    events = []
    eventQuerySet = FightEvent.objects.all()

    for year in range(2023,2026):
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
    return JsonResponse({'events':events})

def aggregateAndParseEventMatchups(event: FightEvent):
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

@require_GET
def vueFightEvent(request):
    #return the next fight event
    #get current day date
    current_date = datetime.now().date()
    #from FightEvent model, get the first event that is after or on the current date
    event = FightEvent.objects.filter(date__gte=current_date).order_by('date').first()
    if event:
        return aggregateAndParseEventMatchups(event)
    return JsonResponse({'No Event Upcoming':None})


@require_GET
def vueAssessment(request,fighterId):
    
    fighterQ = Fighter.objects.filter(id=fighterId)
    if not fighterQ.exists():
        return JsonResponse({'error':'fighter does not exist'})
    
    fighter = fighterQ[0]
    assessmentQ = Assessment.objects.filter(fighter=fighter)
    if not assessmentQ.exists():
        return JsonResponse({'error':'assessment object does not exist'})

    assessment = assessmentQ[0]
    notes = []
    noteQ = Note.objects.filter(assessment=assessment)
    if noteQ.exists():
        notes = [ {'data':note.data,'createdAt':note.createdAt,'id':note.id} for note in noteQ ]
    data = {
        'fighter':model_to_dict(fighter),
        'assessment':model_to_dict(assessment),
        'notes':notes
    }
    return JsonResponse(data)

@require_GET
def get_matchup_comparison(request,matchupId):
    matchup = get_object_or_404(MatchUp,id=matchupId)
    fighter_a = matchup.fighter_a
    fighter_b = matchup.fighter_b
    pick = None
    pickQSet = Pick.objects.filter(matchup=matchup)
    if pickQSet.exists():
        pick = pickQSet[0]
    data = {
        'matchup' :  model_to_dict(matchup),
        'fighter_a' :  model_to_dict(fighter_a),
        'fighter_a_assessment' : model_to_dict(Assessment.objects.get(fighter=fighter_a)),
        'fighter_b' :  model_to_dict(fighter_b),
        'fighter_b_assessment' : model_to_dict(Assessment.objects.get(fighter=fighter_b)),
        'standardEvents':[
            {'name':Event.WIN.label,'value':Event.WIN},
            {'name':Event.ROUNDS_GEQ_ONE_AND_HALF.label,'value':Event.ROUNDS_GEQ_ONE_AND_HALF},
            { 'name':Event.DOES_NOT_GO_THE_DISTANCE.label,'value': Event.DOES_NOT_GO_THE_DISTANCE}
        ],
        'eventLikelihoods': [model_to_dict(e) for e in EventLikelihood.objects.filter(matchup=matchup)],
        'prediction': Prediction.objects.filter(matchup=matchup).first(),
        'pick': model_to_dict(pick)
    }
    """
        how to consume this endpoint data

         data 
            matchup:
                matchup_data
            fighter_a :
                fighter_a data
                assessment
                    data
            fighter_b:
                fighter_b data
                assessment
                    data
            
        
        assessment
            fighter 
            attributes 
            
        
    """


    return JsonResponse(data)

@require_POST
def makePick(request,matchupId):
    """
    
        pick
            matchupId
            event
            prediction: nullable

        prediction
            matchupId
            event 
            likelihood
            justification
    
    """
    matchup = get_object_or_404(MatchUp,id=matchupId)
    inputBody = json.loads(request.body)
    inputBody['matchup'] = matchup.id
    print('make pick => ',inputBody)
    pick = None
    pickQSet = Pick.objects.filter(matchup=matchup)
    pickForm = None
    if pickQSet.exists():
        pick = pickQSet[0]
        pickForm = PickForm(data=inputBody,instance=pick)
    else:
        pickForm = PickForm(data=inputBody)
    if pickForm.is_valid():
        print(pickForm.cleaned_data)
        pick.event = pickForm.cleaned_data['event']
        pick.save()
        return JsonResponse({'pick':model_to_dict(pick)})
    print(pickForm.errors)
    return JsonResponse({'error':'error in data'})