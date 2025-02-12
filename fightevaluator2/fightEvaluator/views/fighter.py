from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,QueryDict
from django.db.models import Q
from django.forms.models import model_to_dict
from django.forms import modelform_factory
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.http.response import HttpResponseBadRequest

from ..models import FightEvent,MatchUp,Fighter,Assessment,Note,WeightClass,Stance
from ..forms import *
import json
import datetime

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

# @require_http_methods(["PATCH"])
def update_fighter2(request,fighterId):
    fighter = get_object_or_404(Fighter,id=fighterId)
    #so now what?
    #there is a key for the attribute name, a value for the attribute value
    fighterUpdateData = json.loads(request.body)
    print(fighterUpdateData)
    #for every key we want to create a form class
    CustomFighterFormClass = modelform_factory(Fighter,fields=fighterUpdateData.keys())#['height','last_name'])
    """
        NOTE 
            ABOUT FORMS
            - WHEN PROVIDING DATA IF THE FIELD IS A REQUIRED FIELD IN THE MODEL
              THEN IT MUST BE PRESENT IN THE DATA
            - IF THE FIELD IS NOT A REQUIRED FIELD IN THE MODEL THEN IT IS OPTIONAL TO
              PROVIDE IN THE DATA
    """
    form = CustomFighterFormClass(data=fighterUpdateData,instance=fighter)
    if form.is_valid():
        print('form is valid!')
        form.save()
        result = {}
        fighter.refresh_from_db()
        for k in fighterUpdateData:
            result[k] = getattr(fighter,k)
        return JsonResponse(result)
    else:
        print(form.errors)
        return JsonResponse({'success':False,'errors':form.errors},status=400)

