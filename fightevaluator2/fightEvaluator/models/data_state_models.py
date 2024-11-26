from django.db import models
# import datetime

class OddsDataState(models.Model):
     staleOrEmpty = models.BooleanField(default=False)
     updating = models.BooleanField(default=False)
     date = models.DateField(default=None,blank=True,null=True)

class FightEventDataState(models.Model):
     staleOrEmpty = models.BooleanField(default=False)
     updating = models.BooleanField(default=False)
     date = models.DateField(default=None,blank=True,null=True)

