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


def get_voice_ana(ID):
  obj = ZakatPosts.objects.filter(id=ID).first()
  video1 = str(obj.video1.url)
  video1 = "C:/Product/FS_1.1/static_cdn" + video1
  video1 = video1.replace('/media/', '/media_root/')
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
  
  # remove traced_model.pt
  shutil.rmtree('C:/Product/FS_1.1/fs/AI/sentiment_ana/traced_model.pt', ignore_errors=True)
  shutil.rmtree("C:/Product/FS_1.1/fs/AI/sentiment_ana/runs", ignore_errors=True)
  # now I need to pass this audio to emotion_detection.py
  obj = audio2emo(audio_path='C:/Product/FS_1.1/fs/AI/sentiment_ana/sample.mp3')
  output = obj.engine()
  return output