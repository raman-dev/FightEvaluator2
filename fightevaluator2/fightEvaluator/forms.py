from django import forms
from django.forms import ModelForm

from .models import Fighter,Assessment


class AssessmentForm(ModelForm):
    class Meta:
        model = Assessment
        fields = ['head_movement','gas_tank','aggression','desire_to_win','striking','chinny','grappling_offense','grappling_defense']


class NoteForm(forms.Form):
    assessment_id = forms.IntegerField(label='Assessment Id')
    data = forms.CharField(label='Data',max_length=256)

class FighterForm(ModelForm):
    class Meta:
        model = Fighter
        fields = ['first_name','last_name','height','weight_class','reach','stance','date_of_birth','wins','losses','draws','img_link']
    

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