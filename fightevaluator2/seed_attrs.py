import json
from fightEvaluator.models import *

data = None
with open("defs.json","r") as f:
    data = json.load(f)

def create():
    for attribName,attribValueStateMap in data.items():
        # print(attribName)
        attribName = attribName.replace('_',' ')
        attribute = Attribute.objects.get(name=attribName)
        # print(attribute)
        print()
        for k,stateDescr in attribValueStateMap.items():
            # print(k,stateDescr)
            value = 0
            if k == "positive":
                value = 3
            elif k == "neutral":
                value = 2
            elif k == "negative":
                value = 1
            
            # print(value,stateDescr["state"])
            #default value = 1
            obj = AttributeValue(
                attribute=attribute,
                value=AttributeValue.ValueChoices[k.upper()],
                value_label=stateDescr["state"],
                description=stateDescr["description"]
            )
            obj.save()
            print(obj)