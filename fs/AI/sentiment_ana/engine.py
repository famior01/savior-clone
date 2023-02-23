'''
Process:
1. Get video ID from Zakat_post.view
2. Get video > convert to audio > pass it to emotion_detection.py
'''

# Imports 
from zakat_posts.models import ZakatPosts
import moviepy.editor as me
import os
from .audio_ana import audio2emo
import shutil
from decouple import config
from notifications.signals import notify
from AI.space_vid_utils import get_audio_of_space_vid


ABSOLUTE_PATH = config('ABSOLUTE_PATH')
USE_PRODUCTION= config('USE_PRODUCTION', cast=bool)
TESTING= config('TESTING', cast=bool)


def get_voice_ana(ID):
  obj = ZakatPosts.objects.filter(id=ID).first()
  video1 = str(obj.video1.url)
  if USE_PRODUCTION: 
    notify.send(obj.creator.user, recipient=obj.creator.user, verb='Your video is being processed')
    get_audio_of_space_vid(video1) #TODO; check whether it is checking mute videos or not  
  else:
    video1 = ABSOLUTE_PATH + video1
    print('************\n\t In Audio Analysis \n\t************')

    # first I need to extract audio from video
    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    video = me.VideoFileClip(video1)
    audio = video.audio
    if audio == None: # if no audio in video
      return "Number first video has no audio"
    else:
      audio.write_audiofile('sample.mp3')

  print("********* Made MP3 file! *********")
  
  # now I need to pass this audio to emotion_detection.py
  obj = audio2emo(audio_path=f'{ABSOLUTE_PATH}/AI/sentiment_ana/sample.mp3')
  output = obj.engine()

  # remove traced_model.pt and runs folder
  shutil.rmtree(f'{ABSOLUTE_PATH}/AI/sentiment_ana/traced_model.pt', ignore_errors=True)
  shutil.rmtree(f"{ABSOLUTE_PATH}/AI/sentiment_ana/runs", ignore_errors=True)

  return output