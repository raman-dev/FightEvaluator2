from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,Http404
from django.db.models import Q
from django.forms.models import model_to_dict,modelform_factory
from django.views.decorators.http import require_GET,require_http_methods
from django.views.generic import TemplateView,DetailView

from ..models import MatchUp,Fighter,Assessment,Note#,Assessment2, Attribute, AttributeValue
from ..forms import *
import json

from django.core.serializers import serialize

@require_GET
def assessment_index(request,fighterId): 
    fighter = get_object_or_404(Fighter,id=fighterId)
    assessment = Assessment.objects.get(fighter=fighter)
    #order in latest note first
    notes = Note.objects.filter(assessment=assessment).order_by('-createdAt')
    nextMatchup = MatchUp.objects.filter(Q(fighter_a=fighter) | Q(fighter_b=fighter)).order_by('event__date').last()
    fighterjson = serialize("json",[fighter])

    context = {
        'fighter':fighter,
        'fighterjson': fighterjson,
        'assessment':assessment,
        'notes':notes,
        'attribs':assessment.attrib_map.items(),
        'nextMatchup':nextMatchup,
    }

    return render(request,"fightEvaluator/assessment2.html",context)

# class Assessment2DetailView(DetailView):
#     model = Assessment2

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         fighter = self.object.fighter
#         oldAssessment = Assessment.objects.get(fighter=fighter)
#         context['fighter'] = fighter
#         context['notes'] = Note.objects.filter(assessment=oldAssessment).order_by('-createdAt')
#         context['nextMatchup'] = MatchUp.objects.filter(Q(fighter_a=fighter) | Q(fighter_b=fighter)).order_by('event__date').last()
#         context['attributes'] = self.object.attributes.all().order_by('-attribute__order')
        
#         attrMap = {}
#         allAttributes = AttributeValue.objects.all().order_by("-value")
        
#         for attr in allAttributes:
#             name = attr.attribute.name
#             # print(name)
#             if name not in attrMap:
#                 attrMap[name] = []
#             attrMap[name].append(attr) 

#         context['attrMap'] = attrMap
#         return context
    
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
def update_assessment2(request,assessmentId):
    
    assessment = get_object_or_404(Assessment,id=assessmentId)
    
    inputBody = json.loads(request.body)
    attributes = [ k for k in inputBody.keys() if k !='id']

    assessmentUpdateData = inputBody

    CustomAssessmentFormClass = modelform_factory(Assessment,fields=attributes)
    customForm = CustomAssessmentFormClass(data=assessmentUpdateData,instance=assessment)
    if customForm.is_valid():#form.is_valid():
        # print('form is valid')
        customForm.save()
        assessment.refresh_from_db()
        model = model_to_dict(assessment)
        result = {}
        for key in attributes:
            result[key] = model[key]
        print(result)
        return JsonResponse(result)
    # else:
        # print('invalid')
    return JsonResponse({'error':'invalid form'})
    # result = model_to_dict(assessment)

@require_http_methods(["PATCH"])
def update_assessment(request):
    #get body parameters from request object
    #convert body bytes to json object
    inputBody = json.loads(request.body)
    # print(inputBody)
    attributes = [ k for k in inputBody.keys() if k !='id']
    
    #need to inverse map values 
    # form = AssessmentForm(inputBody)
    valid_id = inputBody['id']
    #validate valid_id is a valid non-negative integer
    if type(valid_id) != int or valid_id < 0:
        return JsonResponse({'error':'invalid id'})
    assessment = get_object_or_404(Assessment,id=valid_id)
    assessmentUpdateData = inputBody
    assessmentUpdateData.pop('id')

    print(assessmentUpdateData,attributes)
    CustomAssessmentFormClass = modelform_factory(Assessment,fields=attributes)
    customForm = CustomAssessmentFormClass(data=assessmentUpdateData,instance=assessment)
    if customForm.is_valid():#form.is_valid():
        # print('form is valid')
        customForm.save()
        assessment.refresh_from_db()
    else:
        # print('invalid')
        return JsonResponse({'error':'invalid form'})
    # result = model_to_dict(assessment)
    return JsonResponse(model_to_dict(assessment))
