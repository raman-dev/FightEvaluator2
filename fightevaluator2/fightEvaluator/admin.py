from django.contrib import admin
from .models import Fighter,Assessment,Note,MatchUp,FightEvent,MatchUpOutcome
# Register your models here.

@admin.register(FightEvent)
class FightEventAdmin(admin.ModelAdmin):
    list_display = ["title","date","location","link"]

@admin.register(MatchUp)
class MatchUpAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter A")
    def fighterA(obj):
        return obj.fighter_a.first_name.capitalize() + " " + obj.fighter_a.last_name.capitalize()
    @admin.display(description="Fighter B")
    def fighterB(obj):
        return obj.fighter_b.first_name.capitalize() + " " + obj.fighter_b.last_name.capitalize()
    list_display = [fighterA,fighterB,"isprelim","weight_class","scheduled","event"]

@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Name",{"fields":["first_name","middle_name","last_name","nick_name"]}),
        ("Bio",{"fields":["weight_class","height","reach","date_of_birth"]}),
        ("Fight Info",{"fields":["wins","losses","draws","stance"]}),
        ("Links",{"fields":["data_api_link"]})
    ]
    
    @admin.display(description="Fighter Name")
    def fighterName(fighter):
        return fighter.first_name.capitalize() + " " + fighter.last_name.capitalize()
    list_display = ["first_name","last_name","weight_class","wins","losses","draws","stance","date_of_birth"]
    search_fields = ["first_name","last_name"]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        return obj.fighter.first_name.capitalize() + " " + obj.fighter.last_name.capitalize()
    list_display = [fighterName,"head_movement","gas_tank","aggression","desire_to_win","striking","chinny","grappling_offense","grappling_defense"]
    search_fields = ["fighter__first_name","fighter__last_name"]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        return obj.assessment.fighter.first_name.capitalize() + " " + obj.assessment.fighter.last_name.capitalize()
    list_display = [fighterName,"data","createdAt"]

@admin.register(MatchUpOutcome)
class MatchUpOutcomeAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        if not obj.fighter:
            return "Fighter Not Needed"
        return obj.fighter.first_name.capitalize() + " " + obj.fighter.last_name.capitalize()
    list_display = ["outcome","likelihood",fighterName,"matchup"]
    # search_fields = [""]

# admin.site.register(Fighter,FighterAdmin)
# admin.site.register(Assessment,AssessmentAdmin)