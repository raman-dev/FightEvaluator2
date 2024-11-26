from django.db import models

class WeightClass(models.TextChoices):
    NA = "n/a"
    ATOMWEIGHT = "atomweight"
    STRAWWEIGHT = "strawweight"
    FLYWEIGHT = "flyweight"
    BANTAMWEIGHT = "bantamweight"
    FEATHERWEIGHT = "featherweight"
    LIGHTWEIGHT = "lightweight"
    WELTERWEIGHT = "welterweight"
    MIDDLEWEIGHT = "middleweight"
    LIGHT_HEAVYWEIGHT = "light_heavyweight"
    HEAVYWEIGHT = "heavyweight"
    CATCH_WEIGHT = "catch_weight"

class Stance(models.TextChoices):
    NA = "n/a"
    ORTHODOX = "orthodox"
    SOUTHPAW = "southpaw"
    SWITCH = "switch"
    OPEN_STANCE = "open_stance"
    SIDE_STANCE = "side_stance"
    SQUARE_STANCE = "square_stance"

class AttributeQualifier(models.IntegerChoices):
        UNTESTED = (0,"untested")
        NEGATIVE = (1,"negative")
        NEUTRAL = (2,"neutral")
        POSITIVE = (3,"positive")

class Likelihood(models.IntegerChoices):
    UNLIKELY = (5,"Very Unlikely")
    POSSIBLE = (4,"Somewhat Unlikely")
    NEUTRAL = (3,"Neutral")
    LIKELY = (2,"Likely")
    VERY_LIKELY = (1,"Very Likely")
    NOT_PREDICTED = (0,"Not Predicted")


class Event(models.TextChoices):
    WIN = "Win","Fighter wins"  
    GOES_THE_DISTANCE = "Yes","Fight Goes the Distance"
    DOES_NOT_GO_THE_DISTANCE = "No","Fight Does Not Go the Distance"
    
    ROUNDS_GEQ_ZERO_AND_HALF = "Rnds >= 0.5","Fight lasts more than 0.5 rounds"
    ROUNDS_GEQ_ONE_AND_HALF = "Rnds >= 1.5","Fight lasts more than 1.5 rounds"
    ROUNDS_GEQ_TWO_AND_HALF = "Rnds >= 2.5","Fight lasts more than 2.5 rounds"
    ROUNDS_GEQ_THREE_AND_HALF = "Rnds >= 3.5","Fight lasts more than 3.5 rounds"
    ROUNDS_GEQ_FOUR_AND_HALF = "Rnds >= 4.5","Fight lasts more than 4.5 rounds"
    NA = "NA","Not Available" #unset event