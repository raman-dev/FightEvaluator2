from fightEvaluator.models import *

def create_name_indices():
    i = 0
    for f in Fighter.objects.all():
        f.first_name = f.first_name.lower()
        f.last_name = f.last_name.lower()
        f.name_index = f.first_name + "-"+ "-".join(f.last_name.split(" "))
        print(i,f.name_index)
        i+=1
        f.save()

create_name_indices()