from fightEvaluator.models import *


def map_vals():
    """

    WIN = "Win","Fighter wins"
    GOES_THE_DISTANCE = "Yes","Fight Goes the Distance"
    DOES_NOT_GO_THE_DISTANCE = "No","Fight Does Not Go the Distance"

    ROUNDS_GEQ_ZERO_AND_HALF = "Rnds >= 0.5","Fight lasts more than 0.5 rounds"
    ROUNDS_GEQ_ONE_AND_HALF = "Rnds >= 1.5","Fight lasts more than 1.5 rounds"
    ROUNDS_GEQ_TWO_AND_HALF = "Rnds >= 2.5","Fight lasts more than 2.5 rounds"
    ROUNDS_GEQ_THREE_AND_HALF = "Rnds >= 3.5","Fight lasts more than 3.5 rounds"
    ROUNDS_GEQ_FOUR_AND_HALF = "Rnds >= 4.5","Fight lasts more than 4.5 rounds"
    NA = "NA","Not Available" #unset event

    """
    valueMap = {
        "Win": "WIN",
        "Yes": "GOES_THE_DISTANCE",
        "No": "DOES_NOT_GO_THE_DISTANCE",
        "Rnds >= 0.5": "ROUNDS_GEQ_ZERO_AND_HALF",
        "Rnds >= 1.5": "ROUNDS_GEQ_ONE_AND_HALF",
        "Rnds >= 2.5": "ROUNDS_GEQ_TWO_AND_HALF",
        "Rnds >= 3.5": "ROUNDS_GEQ_THREE_AND_HALF",
        "Rnds >= 4.5": "ROUNDS_GEQ_FOUR_AND_HALF",
    }
    for e in EventLikelihood.objects.all():
        newVal = valueMap[e.event]
        print(e)
        e.event = newVal
        print(e)
        print()
        e.save()


map_vals()
