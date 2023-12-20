from django.db import models

class WeightClass(models.TextChoices):
    ATOMWEIGHT = "Atomweight"
    STRAWWEIGHT = "Strawweight"
    FLYWEIGHT = "Flyweight"
    BANTAMWEIGHT = "Bantamweight"
    FEATHERWEIGHT = "Featherweight"
    LIGHTWEIGHT = "Lightweight"
    WELTERWEIGHT = "Welterweight"
    MIDDLEWEIGHT = "Middleweight"
    LIGHT_HEAVYWEIGHT = "Light Heavyweight"
    HEAVYWEIGHT = "Heavyweight"
    CATCH_WEIGHT = "Catch weight"

class Stance(models.TextChoices):
    NA = "N\\/A"
    ORTHODOX = "Orthodox"
    SOUTHPAW = "Southpaw"
    SWITCH = "Switch"
    OPEN_STANCE = "Open Stance"
    SIDE_STANCE = "Side Stance"
    SQUARE_STANCE = "Square Stance"

class AttributeQualifier(models.IntegerChoices):
        UNTESTED = 0
        NEGATIVE = 1
        NEUTRAL = 2
        POSITIVE = 3
    
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
     location = models.CharField(default=None,null=True,max_length=256)#location of event
     link = models.CharField(default=None,null=True,max_length=256)#link to event information

class MatchUp(models.Model):
     fighter_a = models.ForeignKey('Fighter',on_delete=models.CASCADE,related_name="fighter_a")
     fighter_b = models.ForeignKey('Fighter',on_delete=models.CASCADE,related_name="fighter_b")
     #optional number of rounds
     rounds = models.IntegerField(default=3, null=True)
     #optional date of bout
     scheduled = models.DateField(default=None, null=True)
     #optional event 
     event = models.ForeignKey('FightEvent',default=None, null=True,on_delete=models.DO_NOTHING)#don't delete matchup if event is deleted

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

    def __str__(self):
        return self.fighter.first_name + " "+self.fighter.last_name +" | Assessment"

# Create your models here
class Fighter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(default="N/A",max_length=100)
    weight_class = models.CharField(max_length=100,choices=WeightClass.choices)
    
    height = models.IntegerField(default=0)#in inches
    reach = models.IntegerField(default=0)#in inches

    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    stance = models.CharField(default=Stance.NA,null=True,max_length=100,choices=Stance.choices)
    date_of_birth = models.DateField(default=None, null=True)
    data_api_link = models.CharField(max_length=256,null=True)
    img_link = models.CharField(max_length=256,null=True)
    assessment_id = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + str(self.wins) + "," +str(self.losses) + "," + str(self.draws) + ")" + " " + self.weight_class + " " + str(self.height) + " " + str(self.reach) + " " + str(self.stance) + " " + str(self.date_of_birth)