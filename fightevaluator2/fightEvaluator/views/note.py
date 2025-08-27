from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST,require_http_methods

from ..models import Assessment,Note
from ..forms import *
import json
import datetime

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
        note = Note(assessment=assessment,data=form.cleaned_data['data'],tag=form.cleaned_data['tag'])
        note.save()
    else:
        print('invalid')
        #raise validation error
    return JsonResponse(model_to_dict(note))

@require_http_methods(["DELETE"])
def delete_note(_,noteId):
    note = get_object_or_404(Note,id=noteId)
    note.delete()
    return JsonResponse({"noteId":noteId})