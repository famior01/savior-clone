from .face_emo_detection.connector import find_emotion
from .sentiment_ana.get_voice_ana import engin

def Analysis(ID):

  # getting Video emoion analysis
  emotions  = find_emotion(video_id=ID)  # Done
  print(emotions)

  # GETTING VOICE ANALYSIS
  obj = engin(ID)                       # Done
  print(obj)


def object_detection():
  pass # TODO
