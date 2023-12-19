from django.contrib import admin
from .models import Fighter,Assessment
# Register your models here.

class FighterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Name",{"fields":["first_name","last_name","nick_name"]}),
        ("Bio",{"fields":["weight_class","height","reach","date_of_birth"]}),
        ("Fight Info",{"fields":["wins","losses","draws","stance"]}),
        ("Links",{"fields":["data_api_link"]})
    ]
    
    @admin.display(description="Fighter Name")
    def fighterName(fighter):
        return fighter.first_name.capitalize() + " " + fighter.last_name.capitalize()
    list_display = [fighterName,"weight_class","wins","losses","draws","stance","date_of_birth"]



class AssessmentAdmin(admin.ModelAdmin):
    @admin.display(description="Fighter Name")
    def fighterName(obj):
        return obj.fighter.first_name.capitalize() + " " + obj.fighter.last_name.capitalize()
    list_display = [fighterName,"head_movement","gas_tank","aggression","desire_to_win","striking","chinny","grappling_offense","grappling_defense"]

admin.site.register(Fighter,FighterAdmin)
admin.site.register(Assessment,AssessmentAdmin)