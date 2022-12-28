from __future__ import absolute_import, unicode_literals
from .face_emo_detection.engine import find_emotion
from .sentiment_ana.engine import get_voice_ana
from .YOLOv7.engine import Object_Detection
from celery import Celery
from django.conf import settings
from celery import shared_task
# from family_savior.celery import app
from django.contrib import messages
from zakat_posts.models import ZakatPosts

@shared_task()
def AI(ID):
  # messages.info(request, 'Your post has been received, and will be verified and post soon, after the verification by our AI.!')

  print("\n\n***********\t IN the AI function \t***********")
  # getting Video emotion analysis
  face_ana = find_emotion(video_id=ID)  
  if type(face_ana) == str: # if string then return it
    return face_ana

  # # # GETTING VOICE ANALYSIS1
  audio_ana = get_voice_ana(ID)                       
  if type(audio_ana) == str: # if string then return it
    return audio_ana

  # GETTING OBJECT DETECTION
  objects_ana = Object_Detection(ID).engin() # calling the engin function
  if type(objects_ana) == str: # if string then return it
    return objects_ana 

  # COMBINING ALL AI MODELS RESULTS
  Nor_and_add = ((face_ana/10)+(audio_ana/10)+(objects_ana/100)) # normalizing and adding
  print("********face_ana", face_ana, "************************")
  print("******audio_ana", audio_ana, "************************")
  print("*********objects_ana", objects_ana, "************************")
  print("**************Nor_and_add", Nor_and_add, "************************")
  avg = (Nor_and_add//3)*100 # getting average
  print("Average of all******", avg, "************************")
  # return 'Jani how are you, keep doing!'

  if avg>50:
    zp = ZakatPosts.objects.get(id=ID) # delete full object
    zp.varified = avg
    zp.save()
    return avg
  else:
    print("******** average is less than 40 ********")
    return "Abdullah didn't varify your post :(" # object will be delete in view
  