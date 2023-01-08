"""
This file is used to send signals to the user profile app. 
"""
from django.db.models.signals import post_save, pre_delete 
# from django.contrib.auth import get_user_model # this is the user model
from user.models import User
from django.dispatch import receiver # this is the receiver of the signal
from .models import Profile # this is the profile model

@receiver (post_save, sender = User)
def create_profile (sender, instance, created, **kwargs):
  '''
  Whenever a user is created, a profile is created for that user too. 
  sender = User
  instance = the user that was created
  created = boolean, true if the user was created
  '''
  # print('sender', sender, 'instance', instance, 'created', created) 
  if created:
    # create a profile for the user, if user was created
    Profile.objects.create(user = instance)
