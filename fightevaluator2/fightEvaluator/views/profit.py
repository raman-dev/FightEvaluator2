from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Count,Q

@require_GET
def profit_calculator(request):
        return render(request, "fightEvaluator/profit.html")
