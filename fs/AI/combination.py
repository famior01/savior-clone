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

  # COMBINING ALL THE ANALYSIS
  if face_ana and audio_ana and objects_ana:
    print("\n******************\tVerified\t******************\n")
    return 1
  else:
    return 0
    