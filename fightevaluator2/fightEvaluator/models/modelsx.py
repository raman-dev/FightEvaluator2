from django.db import models
from .qualifiers_and_choices import *    

class FightEvent(models.Model):
     title = models.CharField(max_length=256)#name of event     
     date = models.DateField()#date of event
     #one to many relationship one fightevent has many matchups
     location = models.CharField(default=None,null=True,blank=True,max_length=256)#location of event
     link = models.CharField(default=None,null=True,blank=True,max_length=256)#link to event information
     hasResults = models.BooleanField(default=False)
    
     def __str__(self) -> str:
          return self.title + " | " + str(self.date)

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
     fighter_a = models.ForeignKey('Fighter',on_delete=models.SET_NULL,related_name="fighter_a",null=True)
     fighter_b = models.ForeignKey('Fighter',on_delete=models.SET_NULL,related_name="fighter_b",null=True)
     weight_class = models.CharField(default=WeightClass.NA,max_length=100,choices=WeightClass.choices)
     #optional number of rounds
     rounds = models.IntegerField(default=3, null=True,blank=True)
     #optional date of bout
     scheduled = models.DateField(default=None, null=True,blank=True)
     #optional event 
     event = models.ForeignKey('FightEvent',default=None, null=True,blank=True,on_delete=models.CASCADE)#don't delete matchup if event is deleted
     #optional result
     #optional boolean isprelim
     isprelim = models.BooleanField(default=True,null=True,blank=True) 
     outcome = models.ForeignKey('FightOutcome',on_delete=models.DO_NOTHING,default=None,blank=True,null=True)
     inWatchList = models.BooleanField(null=True,blank=True)
     analysisComplete = models.BooleanField(null=True,blank=True,default=False)
     fighter_a_references = models.IntegerField(default=0,null=True,blank=True)
     fighter_b_references = models.IntegerField(default=0,null=True,blank=True)

     def __str__(self) -> str:
          return self.fighter_a.last_name.capitalize() + " vs " + self.fighter_b.last_name.capitalize() + " | " + self.weight_class
    
     def title(self) -> str:
          return self.fighter_a.last_name.capitalize() + " vs " + self.fighter_b.last_name.capitalize()
    
     def title_full(self) -> str:
          return self.fighter_a.name + " vs " + self.fighter_b.name


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