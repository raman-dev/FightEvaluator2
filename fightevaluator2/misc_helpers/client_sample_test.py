from django.test.utils import setup_test_environment
from django.test import Client

setup_test_environment()

def testMakePrediction():
    c = Client()
    putResp = c.put(path='/vue/analysis/make-prediction/1466',data={'event':'ROUNDS_GEQ_ONE_AND_HALF','likelihood':3},content_type='application/json')
    print(putResp.status_code)
    print(putResp.json())

# testMakePrediction()