from .face_emo_detection.engine import find_emotion
from .sentiment_ana.engine import get_voice_ana
from .YOLOv7.engine import Object_Detection

def AI(ID, blur=False):
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
  avg = Nor_and_add//3 # getting average
  print("************************", avg, "************************")
  if avg>60:
    return avg
  else:
    return 0
    