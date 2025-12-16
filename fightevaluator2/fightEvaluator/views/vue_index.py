from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page


# from ..forms import PickForm
from datetime import datetime
from ..models import *
from ..forms import *
import json

PAGE_CACHE_DURATION = 60 * 2

@require_GET
def vueIndex(request,**kwargs):
    """
    Render the Vue.js index page.
    """
    return render(request, 'fightEvaluator/vue_index.html')

@cache_page(PAGE_CACHE_DURATION)#only cache this since it does not change often
@require_GET
def get_event(request,eventId):
    resultSet = FightEvent.objects.filter(pk=eventId)
    if not resultSet:
        return JsonResponse({'No such event':None})
    event = resultSet[0]
    return aggregateAndParseEventMatchups(event)

@cache_page(PAGE_CACHE_DURATION)#only cache this since it does not change often
@require_GET
def vueAllEvents(request):
    events = []
    eventQuerySet = FightEvent.objects.all()

    for year in range(2023,2027):
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

@cache_page(PAGE_CACHE_DURATION)#only cache this since it does not change often
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


# @cache_page(PAGE_CACHE_DURATION)
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
        notes.sort(key=lambda x:x['createdAt'],reverse=True)

    nextMatchup = MatchUp.objects.filter(Q(fighter_a=fighter) | Q(fighter_b=fighter)).order_by('event__date').last()
    
    matchupInfo = None
    if nextMatchup:
        matchupInfo = {
            'id': nextMatchup.id,
            'title': nextMatchup.title(),
        }
    data = {
        'fighter':model_to_dict(fighter),
        'assessment':model_to_dict(assessment),
        'notes':notes,
        'nextMatchup': matchupInfo
    }
    return JsonResponse(data)

# def getPredictionsMap2(predictions,standardEvents,matchup):
#     pass

def getPredictionsMap(predictions,standardEvents,matchup):
    """
        {
            event: {
                likelihood
                label
            }

            win:{
                fighter_id:{
                    likelihood
                    label
                }
            }
        }
    """
    result = {}
    for p in predictions:
        if p.event not in result:
            result[p.event] = {}
        if p.event == 'WIN':
            result[p.event][p.fighter.id] = {'likelihood':p.likelihood,'label':p.get_likelihood_display(),'justification':p.justification}
        else:
            result[p.event] = {'likelihood':p.likelihood,'label':p.get_likelihood_display(),'justification':p.justification}
    
    #default likelihoods 
    for e in standardEvents:
        event = e['value']
        if event not in result:
            if event == Event.WIN:
                result[Event.WIN] = {}
                result[Event.WIN][matchup.fighter_a.id] = {'likelihood': Likelihood.NEUTRAL,'label' : Likelihood.NEUTRAL.label,'justification':""}
                result[Event.WIN][matchup.fighter_b.id] = {'likelihood': Likelihood.NEUTRAL,'label' : Likelihood.NEUTRAL.label,'justification':""}
            else:
                result[event] = {'likelihood': Likelihood.NEUTRAL,'label' : Likelihood.NEUTRAL.label ,'justification':""}
        elif event == Event.WIN:
            if len(result[Event.WIN]) != 2:
                winMap = result[Event.WIN]
                fid = matchup.fighter_a.id
                if fid in winMap:
                    fid = matchup.fighter_b.id
                winMap[fid] = {'likelihood': Likelihood.NEUTRAL,'label' : Likelihood.NEUTRAL.label ,'justification':""}
    return result

@require_http_methods(["PUT"])
def makePrediction(request,matchupId):
    #always replace what is there 
    """
    
        prediction2
            matchup : int
            fighter: int | None
            justification : str
            likelihood: int

    """
    matchup = get_object_or_404(MatchUp,id=matchupId)
    
    inputBody = json.loads(request.body)
    print("input received => ",inputBody)

    #grab prediction2 form
    inputBody['matchup'] = matchup.id
    prediction2Form = Prediction2Form(data=inputBody)
    if prediction2Form.is_valid():
        # return JsonResponse({'prediction':'isValid!'})
        args = {
            'matchup': matchup,
            'event': prediction2Form.cleaned_data['event'],
            'defaults': {
                'matchup': matchup,
                'event': prediction2Form.cleaned_data['event'],
            }
        }
        if 'fighter' in prediction2Form.cleaned_data and prediction2Form.cleaned_data['fighter'] != None:
            fighter = get_object_or_404(Fighter,id=prediction2Form.cleaned_data['fighter'].id)
            args['fighter'] = fighter
            args['defaults']['fighter'] = fighter
        if 'justification' in prediction2Form.cleaned_data:
            args['defaults']['justification'] = prediction2Form.cleaned_data['justification']
        if 'likelihood' in prediction2Form.cleaned_data:
            args['defaults']['likelihood'] = prediction2Form.cleaned_data['likelihood']
        prediction2, created = Prediction2.objects.update_or_create(**args)
        result = model_to_dict(prediction2)
        result['label'] = prediction2.get_likelihood_display()
        # if created:
        #     print("CREATED.prediction2 => ",result)
        # else:
        #     print("UPDATED.prediction2 => ",result)
        return JsonResponse({'prediction':result})
    
    return JsonResponse({'error':prediction2Form.errors})

@cache_page(PAGE_CACHE_DURATION // 2)#half standard duration
@require_GET
def get_matchup_comparison(request,matchupId):
    matchup = get_object_or_404(MatchUp,id=matchupId)
    fighter_a = matchup.fighter_a
    fighter_b = matchup.fighter_b
    pick = None
    pickQSet = Pick.objects.filter(matchup=matchup)
    predictionQSet = Prediction.objects.filter(matchup=matchup)
    standardEvents = [
            {'name':Event.WIN.label,'value':Event.WIN},
            {'name':Event.ROUNDS_GEQ_ONE_AND_HALF.label,'value':Event.ROUNDS_GEQ_ONE_AND_HALF},
            { 'name':Event.DOES_NOT_GO_THE_DISTANCE.label,'value': Event.DOES_NOT_GO_THE_DISTANCE}
    ]

    eventLikelihoodsQSet = EventLikelihood.objects.filter(matchup=matchup)
    prediction2QSet = Prediction2.objects.filter(matchup=matchup)
    # predictionsMap = getPredictionsMap(eventLikelihoodsQSet,standardEvents,matchup)
    predictionsMap2 = getPredictionsMap(prediction2QSet,standardEvents,matchup)

    attribComparison = []
    fighterA_assessment = model_to_dict(Assessment.objects.get(fighter=matchup.fighter_a))
    fighterB_assessment = model_to_dict(Assessment.objects.get(fighter=matchup.fighter_b))
    # print(fighterA_assessment)
    for k in fighterA_assessment.keys():
        if k == 'id' or k == 'fighter':
            continue            
        attribComparison.append((k,fighterA_assessment[k],fighterB_assessment[k]))
    
    if pickQSet.exists():
        pick = pickQSet[0]
    data = {
        'matchup' :  model_to_dict(matchup),
        'fighter_a' :  model_to_dict(fighter_a),
        'fighter_a_assessment' : model_to_dict(Assessment.objects.get(fighter=fighter_a)),
        'fighter_b' :  model_to_dict(fighter_b),
        'fighter_b_assessment' : model_to_dict(Assessment.objects.get(fighter=fighter_b)),
        'fighter_a_notes': [ model_to_dict(n) | {'createdAt':n.createdAt} for n in Note.objects.filter(assessment=Assessment.objects.get(fighter=matchup.fighter_a)).order_by('-createdAt')],
        'fighter_b_notes': [ model_to_dict(n) | {'createdAt':n.createdAt} for n in Note.objects.filter(assessment=Assessment.objects.get(fighter=matchup.fighter_b)).order_by('-createdAt')],
        'standardEvents': standardEvents,
        'predictions': predictionsMap2,
        'prediction': model_to_dict(predictionQSet.first()) if predictionQSet.exists() else {},
        'pick': model_to_dict(pick) if pick else {'event':None,'fighter':None},
        'attribComparison' : attribComparison
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

    if pickQSet.exists():
        pickForm = PickForm(data=inputBody,instance=pickQSet[0])
    else:
        pickForm = PickForm(data=inputBody)
    
    if 'event' not in pickForm.data:
        return JsonResponse({'error':'Error in data'})
    
    if pickForm.data['event'] == None:
        if pickQSet.exists():
            #delete pick
            pick = pickQSet[0]
            pick.delete()
            return JsonResponse({'pick':{'event':None,'fighter':None}})
        return JsonResponse({'msg':'no pick to delete'})
    
    #is_valid returns false if model has unique=True on foreign key so
    #even if i am trying to replace delete is necessary
    if pickForm.is_valid():
        #always replace 
        pick = pickForm.save()
        if pickForm.cleaned_data['event'] != Event.WIN:
            pick.fighter = None
            pick.save()
        #check if has prediction2 
        prediction2QSet = Prediction2.objects.filter(matchup=matchup,event=pick.event)
        if prediction2QSet.exists():
            pick.prediction = prediction2QSet[0]
            pick.save()
        print(pick)
        return JsonResponse({'pick':model_to_dict(pick)})
    print(pickForm.errors)
    return JsonResponse({'error':'error in data'})


    