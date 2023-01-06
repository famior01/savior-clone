"""
This file is used to send signals to the user profile app. 
"""
from django.db.models.signals import post_save, pre_delete # this is the signal that is sent when a user is created
from django.contrib.auth import get_user_model # this is the user model
from django.dispatch import receiver # this is the receiver of the signal
from .models import Profile, Relationship # this is the profile model

@receiver (post_save, sender = get_user_model())
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

@receiver(post_save, sender=Relationship)
def add_to_friends(sender, instance, created, **kwargs):
  """
  if the status of the relationship is accepted, then add the sender and receiver to each other's friends list. 
  sender = Relationship model
  instance = the instance of the relationship model that was created
  created = boolean, true if the relationship was created
  """
  sender_ = instance.sender
  receiver_ = instance.receiver
  if instance.status == 'accepted':
      sender_.friends.add(receiver_.user)
      receiver_.friends.add(sender_.user)
      sender_.save()
      receiver_.save()


@receiver(pre_delete, sender=Relationship)
def remove_from_friends(sender, instance, **kwargs):
  """
  here, it will delete relationship from the profile model's friend list. only if we have deleted from the relationship model
  """
  sender_ = instance.sender
  receiver_ = instance.receiver
  if instance.status == 'accepted':
      sender_.friends.remove(receiver_.user) # receiver is profile, we need to pass user, because friends is a many to many field to user
      receiver_.friends.remove(sender_.user)
      sender_.save()
      receiver_.save()