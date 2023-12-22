from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,QueryDict
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST,require_http_methods

from .models import FightEvent,MatchUp,Fighter,Assessment
from .forms import *
import json
import datetime

# Create your views here.
def index(request):
    #purpose of index
    #show next upcoming fight event
    nextEvent = FightEvent.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    #retreive matchups for next event
    matchups = MatchUp.objects.filter(event=nextEvent)
    #split into main card and prelims
    mainCard = []
    prelims = []
    for matchup in matchups:
        if matchup.isprelim:
            prelims.append(matchup)
        else:
            mainCard.append(matchup)
    context= {
        'event': nextEvent,
        'matchupsList': [mainCard,prelims],
    }
    return render(request, "fightEvaluator/index.html",context)

#search for a fighter
def fighter_search(request):
    #get query params from request object
    search_names = request.GET.get('search').split(' ')
    fname = search_names[0]
    lname = fname
    
    if len(search_names) > 1:
        lname = search_names[1]

    fighterQueryValues = ["id","first_name","last_name"]
    query = Q(first_name__startswith=fname) | Q(last_name__contains=lname)
    if fname != lname:
        query = Q(first_name__startswith=fname) & Q(last_name__contains=lname)
        # fighters = Fighter.objects.filter(Q(first_name__startswith=fname) | Q(last_name__contains=lname))[:5].values(fighterQueryValues)
    # else:
        # fighters = Fighter.objects.filter(first_name__startswith=fname,last_name__contains=lname)[:5].values()
    fighters = Fighter.objects.filter(query)[:5].values(*fighterQueryValues)#*list means non keyword arguments passed in
    return JsonResponse({'fighters':list(fighters)})

@require_POST
def create_fighter(request):
    #get query params from request object
    fighterInput = json.loads(request.body)
    fighterInput['weight_class'] = fighterInput['weight_class'].lower()
    fighterForm = FighterForm(fighterInput)#validate data
    # print(fighterForm)
    if fighterForm.is_valid():
        print('fighter valid input')
        print(fighterForm.cleaned_data)
        fighterForm.save()#save fighter
    else:
        print('invalid fighter input')
    return JsonResponse({'fighter':model_to_dict(fighterForm.instance)})

@require_http_methods(["PATCH"])
def update_fighter(request,fighterId):
    fighter = get_object_or_404(Fighter,id=fighterId)
    #get query params from request object
    fighterInput = json.loads(request.body)
    #since attrs are optional we need to check if they exist
    #validate optional fields if they exist
    

def create_matchup(request):
    #get body parameters from request object
    #convert body bytes to json object
    inputBody = json.loads(request.body)
    form = MatchUpForm(inputBody)#use django form object for data validation
    #takes a querydict class as input querydict is a subclass of dict so a normal dict will suffice
    #create matchup
    matchup = None
    if form.is_valid():
        # print('form is valid')    
        matchup = MatchUp(fighter_a=Fighter.objects.get(id=form.cleaned_data['fighter_a_id']),
                          fighter_b=Fighter.objects.get(id=form.cleaned_data['fighter_b_id']),#get fighter object from id
                          weight_class=form.cleaned_data['weight_class'],
                          rounds=form.cleaned_data['rounds'])
        if form.cleaned_data['scheduled'] != None:
            matchup.scheduled = datetime(form.cleaned_data['scheduled'])
        if form.cleaned_data['event_id'] != None:
            matchup.event = FightEvent.objects.get(id=form.cleaned_data['event_id'])
        if form.cleaned_data['isprelim'] != None:
            matchup.isprelim = form.cleaned_data['isprelim']
        matchup.save()
    else:
        #raise validation error
        print('invalid')
    return JsonResponse(model_to_dict(matchup))

def delete_matchup(request,matchupId):
    # MatchUp.objects.filter(id=matchupId).delete()#delete matchup with id
    #get object 404 if not found
    matchup = get_object_or_404(MatchUp,id=matchupId)
    matchup.delete()
    return JsonResponse({"success":"true"})

def assessment_index(request,fighterId): 
    fighter = get_object_or_404(Fighter,id=fighterId)
    assessment = Assessment.objects.get(fighter=fighter)
    nextMatchup = MatchUp.objects.filter(Q(fighter_a=fighter) | Q(fighter_b=fighter)).order_by('scheduled').first()
    fighterjson = str(model_to_dict(fighter))
    fighterjson = fighterjson.replace('None','null')
    context = {
        'fighter':fighter,
        'fighterjson': fighterjson,
        'assessment':assessment,
        'attribs':assessment.attrib_map.items(),
        'nextMatchup':nextMatchup,
    }
    return render(request,"fightEvaluator/assessment.html",context)

@require_POST
def create_note(request):
    #get body parameters from request object
    #convert body bytes to json object
    inputBody = json.loads(request.body)
    form = NoteForm(inputBody)#use django form object for data validation
    #takes a querydict class as input querydict is a subclass of dict so a normal dict will suffice
    #create matchup
    note = None
    if form.is_valid():
        print('note.form is valid') 
        assessment =get_object_or_404(Assessment,id=form.cleaned_data['assessment_id'])   
        note = Note(assessment=assessment,data=form.cleaned_data['data'])
        note.save()
    else:
        print('invalid')
        #raise validation error
    return JsonResponse({'note':model_to_dict(note)})

@require_http_methods(["DELETE"])
def delete_note(_,noteId):
    note = get_object_or_404(Note,id=noteId)
    note.delete()
    return JsonResponse({"success":"true","noteId":noteId})