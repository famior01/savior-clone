from django.db.models.signals import post_save
from notifications.signals import notify
from .models import ZakatPosts

# This will be called when a new post is created. 
def my_handler(sender, instance, created, **kwargs):
    if created:
        notify.send(instance.author, recipient=instance.author, verb='created a new post')
    
post_save.connect(my_handler, sender=ZakatPosts)
