'''
Process:
1. Get video ID from Zakat_post.view
2. Get video > convert to audio > pass it to emotion_detection.py
'''

# Imports 
from zakat_posts.models import ZakatPosts
import moviepy.editor as me
import os
from .emotion_detection import audio2emo



def engin(ID):
  obj = ZakatPosts.objects.filter(id=ID).first()
  video1 = str(obj.video1.url)
  video1 = "C:/Product/FS_1.1/static_cdn" + video1
  video1 = video1.replace('/media/', '/media_root/')
  print('************\n\t from Sentiment Analysis \n\t', video1, '\n************')

  # first I need to extract audio from video
  os.chdir(os.path.realpath(os.path.dirname(__file__)))
  video = me.VideoFileClip(video1)
  audio = video.audio
  audio.write_audiofile('sample.mp3')
  print("Made MP3 file!")

  # now I need to pass this audio to emotion_detection.py
  obj = audio2emo(audio_path='fs/AI/sentiment_ana/sample.mp3')
  output = obj.engine()
  return output