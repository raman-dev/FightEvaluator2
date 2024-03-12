from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.shortcuts import render,get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse

from ..models import FightEvent,MatchUp,FightOutcome,Prediction
from ..forms import FightEventForm,MatchUpFormMF
import json
import datetime
import re
from .. import scraper

def predictions(request):
    
    context = {}

    return render(request, "fightEvaluator/prediction.html",context)
