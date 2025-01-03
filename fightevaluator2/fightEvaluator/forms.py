from django import forms
from django.forms import ModelForm

from .models import Fighter,Assessment,WeightClass,FightEvent,MatchUp,Event,AttributeQualifier

"""
    **NOTE**************************************************
    IF ALL REQUIRED FIELDS ARE NOT PRESENT FOR A ModelForm,
    THEN FORM.SAVE() WILL NOT WORK
    *********************************************************
"""

class FightEventForm(ModelForm):
    class Meta:
        model = FightEvent
        fields = ['title','date','location','link']


class AssessmentForm(ModelForm):
    class Meta:
        model = Assessment
        fields = ['head_movement','gas_tank','aggression','desire_to_win','striking','chinny','grappling_offense','grappling_defense']


class NoteForm(forms.Form):
    assessment_id = forms.IntegerField(label='Assessment Id')
    data = forms.CharField(label='Data',max_length=256)
    tag = forms.CharField(label='Tag',max_length=8)
    def is_valid(self):
        if not super().is_valid():
            return False
        
        tag = self.cleaned_data['tag']
        # print('tag',tag)
        if tag != 'NEUTRAL' and tag != 'NEGATIVE' and tag !='POSITIVE':
            return False
        self.cleaned_data['tag'] = AttributeQualifier[tag]
        # print(AttributeQualifier.NEGATIVE,AttributeQualifier['NEGATIVE'])
        return True
        
class FighterForm(ModelForm):
    class Meta:
        model = Fighter
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super(FighterForm,self).__init__(*args,**kwargs)
        if 'instance' in kwargs:
            print('we have an instance!!')
            # print(kwargs)
            print(kwargs['instance'])
            
        print('constructor called!')

class MatchUpFormMF(ModelForm):
    class Meta:
        model = MatchUp
        fields = ['fighter_a','fighter_b','weight_class','rounds','event','isprelim','scheduled','inWatchList']

class MatchUpUpdateForm(forms.Form):
    fighter_a_id = forms.IntegerField(label='Fighter A Id',required=False)
    fighter_b_id = forms.IntegerField(label='Fighter B Id',required=False)   
    weight_class = forms.CharField(label='Weight Class',max_length=100,required=False)
    rounds = forms.IntegerField(label='Rounds',initial=3,required=False)

    scheduled = forms.DateField(label='Scheduled',initial=None,required=False)
    event_id = forms.IntegerField(label='Event Id',initial=None,required=False)
    isprelim = forms.BooleanField(label='Is Prelim',initial=True,required=False)
    inWatchList = forms.BooleanField(label='In Watch List',required=False)

    def is_valid(self) -> bool:
        if not super().is_valid():
            # print('invalid!!')
            return False
        
        #check if weight_class is a valid weight_class
        weight_class = self.cleaned_data['weight_class'].lower()
        if weight_class not in WeightClass and len(weight_class) > 0:
            # print('invalid weight_class yo')
            return False
        #valid weight_class string
        self.cleaned_data['weight_class'] = weight_class
        return True

class MatchUpForm(forms.Form):
    fighter_a_id = forms.IntegerField(label='Fighter A Id')
    fighter_b_id = forms.IntegerField(label='Fighter B Id')   
    weight_class = forms.CharField(label='Weight Class',max_length=100)
    rounds = forms.IntegerField(label='Rounds',initial=3)

    scheduled = forms.DateField(label='Scheduled',initial=None,required=False)
    event_id = forms.IntegerField(label='Event Id',initial=None,required=False)
    isprelim = forms.BooleanField(label='Is Prelim',initial=True,required=False)

    def is_valid(self) -> bool:
        # return super().is_valid()
        if not super().is_valid():
            return False
        #check if weight_class is a valid weight_class
        weight_class = self.cleaned_data['weight_class'].lower()
        if weight_class not in WeightClass:
            return False
        #valid weight_class string
        self.cleaned_data['weight_class'] = weight_class
        return True

class MatchUpOutcomeUpdateLikelihood(forms.Form):
    likelihood = forms.IntegerField(label='Likelihood',min_value=1,max_value=5)
    justification = forms.CharField(label='Justification',max_length=1024)

class MatchUpEventLikelihoodForm(forms.Form):
    eventType = forms.CharField(label='Event Type',max_length=100)
    likelihood = forms.IntegerField(label='Likelihood',min_value=1,max_value=5)
    justification = forms.CharField(label='Justification',max_length=1024)
    fighterId = forms.IntegerField(label='Fighter Id',required=False)

    #override is_valid
    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        #check if eventType is a valid eventType
        eventType = self.cleaned_data['eventType'].upper()
        #check if event type is one of the Event types
        isValidType = False
        for validType in Event:
            # print(validType.name,eventType)
            if eventType == validType.name:
                self.cleaned_data['eventType'] = eventType
                isValidType = True
                break
        # print('isValidType=>',isValidType)
        fighterId = self.cleaned_data['fighterId']
        if fighterId != 0:
            if not Fighter.objects.filter(id=fighterId).exists():
                return False
        return isValidType

class EventPredictionForm(forms.Form):
    eventType = forms.CharField(label='Event Type',max_length=100)
    fighterId = forms.IntegerField(label='Fighter Id',required=False)

    #override is_valid
    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        #check if eventType is a valid eventType
        eventType = self.cleaned_data['eventType'].upper()
        #check if event type is one of the Event types
        isValidType = False
        for validType in Event:
            # print(validType.name,eventType)
            if eventType == validType.name:
                self.cleaned_data['eventType'] = eventType
                isValidType = True
                break
        # print('isValidType=>',isValidType)
        fighterId = self.cleaned_data['fighterId']
        if fighterId != 0:
            if not Fighter.objects.filter(id=fighterId).exists():
                return False
        return isValidType