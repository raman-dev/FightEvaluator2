from fightEvaluator.models import *
from fightEvaluator.forms import *

f = Fighter.objects.get(pk=2166)
form = FighterForm(data={'data_api_link':'bs'},instance=f)

# print(form.is_valid())
# print(form.errors)
# print(form.data)
# form.save()
# print(form.error_messages)
print(form.is_valid())
print(form.errors)