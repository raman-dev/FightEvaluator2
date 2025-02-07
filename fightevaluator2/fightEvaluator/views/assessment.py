from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,Http404
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.http import require_GET,require_http_methods
from django.views.generic import TemplateView

from ..models import MatchUp,Fighter,Assessment,Note,WeightClass,Stance
from ..forms import *
import json
from .fighter import getFighterJSON

@require_GET
def assessment_index(request,fighterId): 
    fighter = get_object_or_404(Fighter,id=fighterId)
    assessment = Assessment.objects.get(fighter=fighter)
    #order in latest note first
    notes = Note.objects.filter(assessment=assessment).order_by('-createdAt')
    nextMatchup = MatchUp.objects.filter(Q(fighter_a=fighter) | Q(fighter_b=fighter)).order_by('event__date').last()
    fighterjson = getFighterJSON(fighter)
    fighterjson = str(fighterjson)#need string for template writing
    fighterjson = fighterjson.replace('None','null')

    context = {
        'fighter':fighter,
        'fighterjson': fighterjson,
        'assessment':assessment,
        'notes':notes,
        'attribs':assessment.attrib_map.items(),
        'nextMatchup':nextMatchup,
    }

    return render(request,"fightEvaluator/assessment2.html",context)

"""

    class MyView(View):
        override methods for http get,patch,post,put,delete
    
    class MyDetailView(DetailView):
        override methods 
        specify model to circumvent having to specifiy template names explicitly

        model = MyModel
        #template name will be inferred by django
            # templates/app/modelnamelowercase_detail.html
            # 
    

    Assessment (model):
        fighter
        listOf(Attribute)    

    Attribute(model):
        listOf(AttributeValue)
    
    AttributeValue(model):
        value   #higher is better
        value_label
        description

        #ordering_by_value
"""

@require_http_methods(["PATCH"])
def update_assessment(request):
    #get body parameters from request object
    #convert body bytes to json object
    inputBody = json.loads(request.body)
    # print(inputBody)
    #need to inverse map values 
    form = AssessmentForm(inputBody)
    valid_id = inputBody['id']
    #validate valid_id is a valid non-negative integer
    if type(valid_id) != int or valid_id < 0:
        return JsonResponse({'error':'invalid id'})
    assessment = None
    if form.is_valid():
        # print('form is valid')
        # print(form.cleaned_data)
        assessment = get_object_or_404(Assessment,id=valid_id)
        #write all values to assessment
        assessment.head_movement = form.cleaned_data['head_movement']
        assessment.gas_tank = form.cleaned_data['gas_tank']
        assessment.aggression = form.cleaned_data['aggression']
        assessment.desire_to_win = form.cleaned_data['desire_to_win']
        assessment.striking = form.cleaned_data['striking']
        assessment.chinny = form.cleaned_data['chinny']
        assessment.grappling_offense = form.cleaned_data['grappling_offense']
        assessment.grappling_defense = form.cleaned_data['grappling_defense']
        assessment.save()
    else:
        # print('invalid')
        return JsonResponse({'error':'invalid form'})
    # result = model_to_dict(assessment)
    return JsonResponse(model_to_dict(assessment))
