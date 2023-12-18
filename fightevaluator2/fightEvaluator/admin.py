from django.contrib import admin
from .models import Fighter
# Register your models here.

class FighterAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Name",{"fields":["first_name","last_name","nick_name"]}),
        ("Bio",{"fields":["weight_class","height","reach","date_of_birth"]}),
        ("Fight Info",{"fields":["wins","losses","draws","stance"]}),
        ("Links",{"fields":["data_api_link"]})
    ]

admin.site.register(Fighter,FighterAdmin)