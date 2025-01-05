from fightEvaluator.models import *
from fightEvaluator.forms import *

def test():
    f = Fighter.objects.get(pk = 2166)
    form  = FighterForm(data = {'data_api_link':'link'},instance=f)
    print(form.is_valid())
    print(form.errors)
test()