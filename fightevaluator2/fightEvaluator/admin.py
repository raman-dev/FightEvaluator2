from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ["name","total","count","ratio_percent","type"]

@admin.register(Assessment2)
class AssessmentAdmin(admin.ModelAdmin):
    @admin.display
    def mAttributes(self):
        result = []
        for attribM in self.attributes.all():
            result.append(attribM.__str__())
        return result
    filter_horizontal = ["attributes"]
    list_display = ["id","fighter",mAttributes]
    autocomplete_fields = ["fighter"]

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):

    @admin.display(description="Attribute possible values")
    def attrib_values(self):
        # result = []
        return list(AttributeValue.objects.filter(attribute=self).order_by("-value"))
        # return result
    list_display = ["name",attrib_values]

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ["attribute","value_label","description","value"]

@admin.register(FightEvent)
class FightEventAdmin(admin.ModelAdmin):
    list_display = ["title","date","location","link","id"]

@admin.register(MatchUp)
class MatchUpAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter A")
    def fighterA(obj):
        return obj.fighter_a.first_name.capitalize() + " " + obj.fighter_a.last_name.capitalize()
    @admin.display(description="Fighter B")
    def fighterB(obj):
        return obj.fighter_b.first_name.capitalize() + " " + obj.fighter_b.last_name.capitalize()
    
    @admin.display(description="Reference Ratio")
    def referenceRatio(obj):
        return str(obj.fighter_a_references) + ":" +str(obj.fighter_b_references)

    list_display = [fighterA,fighterB,"isprelim","weight_class","analysisComplete","event__date","event"]

@admin.register(MatchUp2)
class MatchUpAdmin2(admin.ModelAdmin):
    @admin.display(description="Fighter A")
    def fighterA(obj):
        return obj.fighter_a.first_name.capitalize() + " " + obj.fighter_a.last_name.capitalize()
    @admin.display(description="Fighter B")
    def fighterB(obj):
        return obj.fighter_b.first_name.capitalize() + " " + obj.fighter_b.last_name.capitalize()

    list_display = [fighterA,fighterB,"is_prelim","weight_class","analysis_complete","event__date","event"]


@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Name",{"fields":["first_name","middle_name","last_name","nick_name","name_index"]}),
        ("Bio",{"fields":["weight_class","height","reach","date_of_birth"]}),
        ("Fight Info",{"fields":["wins","losses","draws","stance"]}),
        ("Links",{"fields":["data_api_link"]})
    ]
    
    @admin.display(description="Fighter Name")
    def fighterName(fighter):
        return fighter.first_name.capitalize() + " " + fighter.last_name.capitalize()
    list_display = ["first_name","last_name","weight_class","wins","losses","draws","stance","date_of_birth","name_index"]
    search_fields = ["first_name","last_name","name_index"]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        return obj.fighter.first_name.capitalize() + " " + obj.fighter.last_name.capitalize()
    list_display = [fighterName,"head_movement","gas_tank","aggression","desire_to_win","striking","chinny","grappling_offense","grappling_defense"]
    search_fields = ["fighter__first_name","fighter__last_name"]
    autocomplete_fields = ["fighter"]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        return obj.assessment.fighter.first_name.capitalize() + " " + obj.assessment.fighter.last_name.capitalize()
    list_display = [fighterName,"data","createdAt"]


@admin.register(Prediction2)
class Prediction2Admin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        if not obj.fighter:
            return "--"
        return obj.fighter.first_name.capitalize() + " " + obj.fighter.last_name.capitalize()
    
    list_display = ["event","likelihood",fighterName,"matchup"]


@admin.register(EventLikelihood)
class EventLikelihoodAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        if not obj.fighter:
            return "--"
        return obj.fighter.first_name.capitalize() + " " + obj.fighter.last_name.capitalize()
    
    list_display = ["event","likelihood",fighterName,"matchup"]

@admin.register(Prediction)
class Prediction(admin.ModelAdmin):

    @admin.display(description="Event Likelihood")
    def eventLikelihood(obj):
        return obj.prediction.get_likelihood_display()

    @admin.display(description="Predicted Event")
    def event(obj):
        return obj.prediction.event

    @admin.display(description="Fighter Name")
    def fighter(obj):
        if not obj.prediction.fighter:
            return "Fighter Not Needed"
        return obj.prediction.fighter.first_name.capitalize() + " " + obj.prediction.fighter.last_name.capitalize()
    list_display = ["matchup",fighter,event,eventLikelihood,"isCorrect","isGamble","matchup__event"]

@admin.register(FightOutcome)
class FightOutcomeAdmin(admin.ModelAdmin):
    @admin.display(description="Winner")
    def winnerName(obj):
        if not obj.winner:
            return "No Winner"
        return obj.winner.name
    list_display = ["method","time","final_round",winnerName]
    # search_fields = ["matchup__fighter_a__first_name","matchup__fighter_a__last_name","matchup__fighter_b__first_name","matchup__fighter_b__last_name"]

@admin.register(OddsDataState)
class OddsDataStateAdmin(admin.ModelAdmin):
    list_display = ["date","updating","staleOrEmpty"]


@admin.register(FightEventDataState)
class FightDataStateAdmin(admin.ModelAdmin):
    list_display = ["date","updating","staleOrEmpty"]


# @admin.register(Prediction2)
# class Prediction2Admin(admin.ModelAdmin):
#     @admin.display
#     def matchup_title(self):
#         return self.matchup.title()
#     list_display = [matchup_title,"event","likelihood","correct"]

