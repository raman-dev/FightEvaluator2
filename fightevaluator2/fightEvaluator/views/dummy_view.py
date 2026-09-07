from datetime import datetime

from django.forms import modelformset_factory, modelform_factory
from django.http import JsonResponse

from ..models import *
from ..forms import *

def modelform_instance_test(request):
    f = Fighter.objects.get(pk = 2166)
    form  = FighterForm(data = {'data_api_link':'link'},instance=f)
    print(form.is_valid())
    print(form.errors)

    return  JsonResponse({'result':'fucked!'})

def modelformfactory_test(request):
    f = Fighter.objects.get(pk=2166)
    # form = FighterForm(data={'data_api_link': 'link'}, instance=f)
    CustomFormClass = modelform_factory(Fighter,fields=["data_api_link","date_of_birth","weight_class"])
    form = CustomFormClass(data={'data_api_link':'some_api_link','date_of_birth':datetime.today().date(),'weight_class':'light_heavyweight'})
    print(form.is_valid())
    print(form.errors)

    return JsonResponse({'result': 'fucked!'})
