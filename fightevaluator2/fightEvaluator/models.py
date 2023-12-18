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

# Create your models here.
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