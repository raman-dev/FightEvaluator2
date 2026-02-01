from django.db import models
from .qualifiers_and_choices import *
from django.db.models import Index, Func,Value, UniqueConstraint
from django.db.models.functions import Concat
from .attributes import AttributeValue

class Note(models.Model):
    assessment = models.ForeignKey('Assessment',on_delete=models.CASCADE)
    # assessment2 = models.ForeignKey('Assessment2',on_delete=models.DO_NOTHING,default=None,blank=True,null=True)
    data = models.CharField(null=True,blank=True,max_length=256)
    tag = models.IntegerField(default=AttributeQualifier.NEUTRAL,choices=AttributeQualifier)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
         return self.data + " | " + str(self.createdAt)

class Assessment2(models.Model):
    #when the fighter is deleted the corresponding assessment is also deleted
    fighter = models.ForeignKey('Fighter',on_delete=models.CASCADE)
    # attributes = models.ManyToManyField(AttributeValue,
    #                                     through="AssessmentAttribValue",
    #                                     default=None,blank=True)
    
    def __str__(self):
        return self.fighter.name

class AssessmentAttribValue(models.Model):
    assessment = models.ForeignKey('Assessment2',on_delete=models.CASCADE)
    attribute = models.ForeignKey('Attribute',on_delete=models.CASCADE)
    attribute_value = models.ForeignKey('AttributeValue',on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=["assessment","attribute_value"],name="unique_assessment_value")]


    # def save(self,*args,**kwargs):
    #     print('calling save',self)
    #     super(AssessmentAttribValue,self).save(*args,**kwargs)

class Assessment(models.Model):
    #when the fighter is deleted the corresponding assessment is also deleted
    fighter = models.ForeignKey('Fighter',on_delete=models.CASCADE,blank=True)
    #blank=True means the a form may have these as blank but a model instance cannot
    head_movement = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)
    gas_tank = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)
    aggression = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)
    desire_to_win = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)
    striking = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)
    chinny = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)
    grappling_offense = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)
    grappling_defense = models.IntegerField(default=AttributeQualifier.UNTESTED,choices=AttributeQualifier,blank=True)

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

    name_index = models.CharField(default="",max_length=256)

    class Meta:
        indexes = [
            Index(fields=["name_index"],name="full_name_index")
        ]
    
    def __save__(self,**kwargs):
        self.name_index = self.first_name + '-'+self.last_name
        super.save(**kwargs)
        

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

    ratio = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    total = models.IntegerField(default=-1)

    @property
    def ratio_percent(self):
        return str(round(100 * (self.ratio),2)) + "%"

    def __str__(self):
        if self.total == -1:
            return "no quantities"
        return self.name + "| Ratio : " + str(self.count) + "/" + str(self.total)# +" | Percentage: " + str(self.ratio)

class EventStat(models.Model):
    #store stats for predictions and correct predictions
    event = models.ForeignKey('FightEvent',on_delete=models.CASCADE)
    predictions = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)

    @property
    def accuracy(self):
        ratio = self.correct/self.predictions
        if self.predictions == 0:
            return "0%"
        return str(round(100 * (ratio),2)) + "%"

class MonthlyEventStats(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()

    events = models.IntegerField(default=0)
    predictions = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)

    @property
    def accuracy(self):
        if self.predictions == 0:
            return "0%"
        ratio = self.correct/self.predictions
        return str(round(100 * ratio,2)) + "%"

    class Meta:
        # unique_together = (('year', 'month'),)
        constraints = [
            UniqueConstraint(fields=["year","month"],name="unique_year_month")
        ]

    def __str__(self):
        return str(self.year) + "-" + str(self.month) + " | Events: " + str(self.events) + " | Predictions: " + str(self.predictions) + " | Correct: " + str(self.correct) + " | Accuracy: " + self.accuracy + "%"
    """
        how to store a stat 
            what is a stat
                a stat is a or all
                    count
                    frequency
                    percentage

        how to store arbitrary stat
            name 
            value_type
            value

            integer field
            float field
        what if we want to store multiple stats together?
            you wouldn't 
            you would have a forein key to a stat aggregate
            from a stat object
        
            Stat
                name
                label
                value_type
                value

            naming convention?    
            StatAggregate
                name
                label
                stats -> many to many stats
            
            need monthly event stats for predictions 
                name:year-month-stats 
                label: January 2024
                stats: many to many to stat 
            
            or less generalized

            MonthlyEventStats
                primary_key(year: int,month: int)
                eventCount: int
                predictions: int
                correct: int
                accuracy: float 
    """
    
