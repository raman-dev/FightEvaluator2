from django.db import models
from django import forms
import datetime

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
    
class Note(models.Model):
    assessment = models.ForeignKey('Assessment',on_delete=models.CASCADE)
    data = models.CharField(null=True,blank=True,max_length=256)
    tag = models.IntegerField(default=AttributeQualifier.NEUTRAL,choices=AttributeQualifier)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
         return self.data + " | " + str(self.createdAt)

class Note2(models.Model):
    data = models.CharField(null=True,blank=True,max_length=256)
    tag = models.IntegerField(default=AttributeQualifier.NEUTRAL,choices=AttributeQualifier)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
         return self.data + " | " + str(self.createdAt)

class AssessmentNote(Note2):
     owner = models.ForeignKey('Assessment',on_delete=models.CASCADE)
    
class MatchupNote(Note2):
     owner = models.ForeignKey('MatchUp',on_delete=models.CASCADE)

class FightEvent(models.Model):
     title = models.CharField(max_length=256)#name of event     
     date = models.DateField()#date of event
     #one to many relationship one fightevent has many matchups
     location = models.CharField(default=None,null=True,blank=True,max_length=256)#location of event
     link = models.CharField(default=None,null=True,blank=True,max_length=256)#link to event information
     hasResults = models.BooleanField(default=False)
    
     def __str__(self) -> str:
          return self.title + " | " + str(self.date)


class Assessment(models.Model):
    #when the fighter is deleted the corresponding assessment is also deleted
    fighter = models.ForeignKey('Fighter',on_delete=models.CASCADE)
    head_movement = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)
    gas_tank = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)
    aggression = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)
    desire_to_win = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)
    striking = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)
    chinny = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)
    grappling_offense = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)
    grappling_defense = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier)

    @property
    def attrib_map(self):
        return {
            'head_movement':self.get_head_movement_display(),
            'gas_tank':self.get_gas_tank_display(),
            'aggression':self.get_aggression_display(),
            'desire_to_win':self.get_desire_to_win_display(),
            'striking':self.get_striking_display(),
            'chinny':self.get_chinny_display(),
            'grappling_offense':self.get_grappling_offense_display(),
            'grappling_defense':self.get_grappling_defense_display()
        }

    def __str__(self):
        return self.fighter.first_name + " "+self.fighter.last_name +" | Assessment"

# Create your models here
class Fighter(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(default="",max_length=100,null=True,blank=True)#optional
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(default="N/A",max_length=100,null=True,blank=True)#optional
    weight_class = models.CharField(max_length=100,choices=WeightClass.choices) 
    
    height = models.IntegerField(default=0)#in inches
    reach = models.IntegerField(default=0)#in inches

    wins = models.IntegerField(default=0,null=True,blank=True)
    losses = models.IntegerField(default=0,null=True,blank=True)
    draws = models.IntegerField(default=0,null=True,blank=True)

    stance = models.CharField(default=Stance.NA,null=True,blank=True,max_length=100,choices=Stance.choices)
    date_of_birth = models.DateField(default=None, null=True,blank=True)
    data_api_link = models.CharField(default="",max_length=256,null=True,blank=True)
    img_link = models.CharField(max_length=256,null=True,blank=True)
    assessment_id = models.IntegerField(default=0,null=True,blank=True)#old field used for migrating data

    @property
    def record(self):
        return str(self.wins) + "-" + str(self.losses) + "-" + str(self.draws)

    @property
    def name(self):
        return self.first_name.capitalize() + " " + self.last_name.capitalize()
    
    @property
    def name_unmod(self):
         return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + str(self.wins) + "," +str(self.losses) + "," + str(self.draws) + ")" + " " + self.weight_class + " " + str(self.height) + " " + str(self.reach) + " " + str(self.stance) + " " + str(self.date_of_birth)

class FightOutcome(models.Model):    
    class Outcomes(models.TextChoices):
        KO = "KO/TKO","Knockout or Technical Knockout"
        SUBMISSION = "Sub","Submission"
        DECISION = "UD/SD/MD","Unanimous Decision/Split Decision/Majority Decision"
        DRAW = "Draw","Draw"
        NO_CONTEST = "NC","No Contest"
        NA = "N/A","Not Available"

    # matchup = models.ForeignKey('MatchUp',on_delete=models.CASCADE)
    #final round
    final_round = models.IntegerField(default=0)
    #stoppage time
    time = models.CharField(default=None,null=True,blank=True,max_length=256)
    #stoppage method
    method = models.CharField(choices=Outcomes.choices,max_length=256,default=Outcomes.NA)
    #winner if there is one
    winner = models.ForeignKey('Fighter',default=None,null=True,blank=True,on_delete=models.CASCADE,related_name="winner")

    def __str__(self):
        return self.method + " " + self.time + " " + str(self.final_round) +"/" +"|" + ("" if not self.winner else str(self.winner.name))

class MatchUp(models.Model):
     class MatchUpResult(models.TextChoices):
            WIN = "Win"
            LOSS = "Loss"
            DRAW = "Draw"
            NO_CONTEST = "No Contest"
            CANCELLED = "Cancelled"
            POSTPONED = "Postponed"
            UPCOMING = "Upcoming"
            NA = "N/A"

    #  created_at = models.DateField(auto_now_add=True)
     fighter_a = models.ForeignKey('Fighter',on_delete=models.CASCADE,related_name="fighter_a")
     fighter_b = models.ForeignKey('Fighter',on_delete=models.CASCADE,related_name="fighter_b")
     weight_class = models.CharField(default=WeightClass.NA,max_length=100,choices=WeightClass.choices)
     #optional number of rounds
     rounds = models.IntegerField(default=3, null=True,blank=True)
     #optional date of bout
     scheduled = models.DateField(default=None, null=True,blank=True)
     #optional event 
     event = models.ForeignKey('FightEvent',default=None, null=True,blank=True,on_delete=models.DO_NOTHING)#don't delete matchup if event is deleted
     #optional result
     #optional boolean isprelim
     isprelim = models.BooleanField(default=True,null=True,blank=True) 
     outcome = models.ForeignKey('FightOutcome',on_delete=models.DO_NOTHING,default=None,blank=True,null=True)
     inWatchList = models.BooleanField(null=True,blank=True)

     def __str__(self) -> str:
          return self.fighter_a.last_name.capitalize() + " vs " + self.fighter_b.last_name.capitalize() + " | " + self.weight_class
    
     def title(self) -> str:
          return self.fighter_a.last_name.capitalize() + " vs " + self.fighter_b.last_name.capitalize()


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

class EventLikelihood(models.Model):
    matchup = models.ForeignKey('MatchUp',on_delete=models.CASCADE)
    
    event = models.CharField(choices=Event.choices,max_length=256)
    eventType = models.CharField(default=None,null=True,blank=True,max_length=256)#helper
    likelihood = models.IntegerField(default=Likelihood.NOT_PREDICTED,null=True,blank=True,choices=Likelihood.choices)
    justification = models.CharField(default=None,null=True,blank=True,max_length=1024)
    
    fighter = models.ForeignKey('Fighter',default=None,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        if self.fighter != None:
            return self.fighter.name +" " + str(self.event) + " => " + self.get_likelihood_display()
        return str(self.event) + "|" + self.get_likelihood_display()
    
    def predictionDisplay(self):
         if self.fighter != None:
              return self.fighter.name + " " + str(self.event)
         return self.get_event_display()

#only 1 prediction per matchup
class Prediction(models.Model):


    matchup = models.ForeignKey('MatchUp',on_delete=models.CASCADE)
    prediction = models.ForeignKey('EventLikelihood',on_delete=models.CASCADE)
    isGamble = models.BooleanField(default=False) #if the prediction is a gamble or an prediction based on analysis
    isCorrect = models.BooleanField(default=None,null=True,blank=True)

    def __str__(self):
        #return what event is predicted and the likelihood
        if self.prediction.fighter != None:
             return self.prediction.fighter.name +", " + str(self.prediction.event) + "|" + str(self.prediction.get_likelihood_display())
        return str(self.prediction.event) + "|" + str(self.prediction.get_likelihood_display())

