from django.db import models
from .qualifiers_and_choices import *

class Note(models.Model):
    assessment = models.ForeignKey('Assessment',on_delete=models.CASCADE)
    assessment2 = models.ForeignKey('Assessment2',on_delete=models.DO_NOTHING,default=None,blank=True,null=True)
    data = models.CharField(null=True,blank=True,max_length=256)
    tag = models.IntegerField(default=AttributeQualifier.NEUTRAL,choices=AttributeQualifier)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
         return self.data + " | " + str(self.createdAt)

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


class Stat(models.Model):
    class StatTypes (models.TextChoices):
        fight_outcome = "fight_outcome"
        probability = "probability"
        general = "general"

    name = models.CharField(max_length=128)
    label = models.CharField(default="",max_length=256)
    type = models.CharField(choices=StatTypes.choices,default=None,blank=True,null=True,max_length=128)

    # ratio = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    total = models.IntegerField(default=-1)

    @property
    def ratio(self):
        return self.count/self.total

    def __str__(self):
        if self.total == -1:
            return "no quantities"
        return self.name + "| Ratio : " + str(self.count) + "/" + str(self.total)# +" | Percentage: " + str(self.ratio)