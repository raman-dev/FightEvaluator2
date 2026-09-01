from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Fighter,Assessment

#only on specific model post_save receiver will fire
# @receiver(post_save,sender=Fighter)
#no longer need this 
def fighter_save_receiver(sender,instance,created,**kwargs):
    # print(f"FighterSaveReceiver called!")
    if created:
        # print(f"FighterSaveReceiver: \n\t Instance created.")
        # t = Assessment(fighter=instance)
        # t.save()
        pass