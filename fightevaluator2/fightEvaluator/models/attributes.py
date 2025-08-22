from django.db import models
from django.db.models import UniqueConstraint

class Attribute(models.Model):
    name = models.CharField(max_length=128)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-order"]

class AttributeValue(models.Model):
    class ValueChoices(models.IntegerChoices):
        POSITIVE = 3,"POSITIVE"
        NEUTRAL = 2,"NEUTRAL"
        NEGATIVE = 1,"NEGATIVE"
        UNTESTED = 0,"UNTESTED"

    attribute = models.ForeignKey('Attribute',on_delete=models.CASCADE)
    value = models.IntegerField(default=ValueChoices.UNTESTED,choices=ValueChoices.choices)
    value_label = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    
    class Meta:
        constraints = [UniqueConstraint(fields=["attribute","value"],name="unique_attribute_value")]
    def __str__(self):
        return self.attribute.name +"|"+ self.value_label

