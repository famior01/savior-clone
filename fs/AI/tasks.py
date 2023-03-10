from __future__ import absolute_import, unicode_literals
from AI.face_emo_detection.engine import find_emotion
from AI.sentiment_ana.engine import get_voice_ana
from AI.object_detection.engine import Object_Detection
from celery import Celery
from django.conf import settings
from celery import shared_task
from django.contrib import messages
from zakat_posts.models import ZakatPosts
# from django.contrib.auth.models import User
from user.models import User
from notifications.signals import notify


@shared_task()
def notify_before_posting(ID):  
  zp = ZakatPosts.objects.get(id=ID) # delete full object
  notify.send(zp.creator.user, recipient=zp.creator.user, verb='Abdullah (AI) is checking your post which might takes more than an hour, after evaluation you will be notified with status of your post. Please wait!')



@shared_task()
def AI(ID):
  zp = ZakatPosts.objects.get(id=ID)
  print("\n\n***********\t IN the AI function \t***********")
  # getting Video emotion analysis
  notify.send(zp.creator.user, recipient=zp.creator.user, verb='in AI function')
  face_ana = find_emotion(video_id=ID)  
  if type(face_ana) == str: # if string then return it
    return face_ana
  notify.send(zp.creator.user, recipient=zp.creator.user, verb='after faec_ana')
  
  # # # GETTING VOICE ANALYSIS1
  audio_ana = get_voice_ana(ID)                       
  if type(audio_ana) == str: # if string then return it
    return audio_ana
  notify.send(zp.creator.user, recipient=zp.creator.user, verb='after audio_ana')

  # GETTING OBJECT DETECTION
  objects_ana = Object_Detection(ID).engin() # calling the engin function
  if type(objects_ana) == str: # if string then return it
    return objects_ana 
  notify.send(zp.creator.user, recipient=zp.creator.user, verb='in AI function')
  

  # COMBINING ALL AI MODELS RESULTS
  Nor_and_add = ((face_ana/10)+(audio_ana/10)+(objects_ana/100)) # normalizing and adding
  print("********face_ana", face_ana, "************************")
  print("******audio_ana", audio_ana, "************************")
  print("*********objects_ana", objects_ana, "************************")
  print("**************Nor_and_add", Nor_and_add, "************************")
  avg = (Nor_and_add/3)*100 # getting average
  print("Average of all******", avg, "************************")
  notify.send(zp.creator.user, recipient=zp.creator.user, verb=f'got this average {avg}')
  if avg>50:
    zp = ZakatPosts.objects.get(id=ID) # delete full object
    zp.varified = avg
    notify.send(zp.creator.user, recipient=zp.creator.user, verb=f'Abdullah (AI) has varified your post with {zp.varified}%, and posted.')
    zp.save()
    return avg
  else:
    '''Saving the post in database, for future training of AI, but not posting it'''
    zp = ZakatPosts.objects.get(id=ID) # delete full object
    zp.varified = avg
    notify.send(zp.creator.user, recipient=zp.creator.user, verb='Sorry! Abdullah (AI) did not varify your post, and did not post it.')
    zp.save()
    return avg
    # return "NOT VARIFIED" # SO THAT IT BALANCE POST NUMBER
