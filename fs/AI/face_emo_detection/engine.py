# THIS FILE WILL GET ID FROM COMBINATION.PY
'''
Some Conditions:
1. The video should be in mp4 format.
2. The video should be in 16:9 ratio.
3. The video should be in 720p or 1080p.
4. Voice should be clear and in Urdu or English.
5. Seeker will state his/her problem in the video, and every member
will appear in the video, one at a time, without saying anything.
6. video should not be recorded in the gathering of the Seeker family, 
  1. There will be more distance btw camera and Seeker's family.
  2. Emotion detection will mess up with alot of people.
  3. if I apply face detection, then it won't be apply to capture clear image. because of the distance. so for now emotion from frames are fine. If found better algorithm, then we would use it.
7. video should be in 16:9 ratio
'''

from AI.face_emo_detection.get_frames import Get_frames
from AI.face_emo_detection.find_similar_faces import GatherSimilarFaces
from AI.face_emo_detection.emotion_detection import Analyze_pics
from AI.face_emo_detection.img_purification import  Purification
import os
import shutil
from decouple import config

ABSOLUTE_PATH = os.environ.get('ABSOLUTE_PATH')

def find_emotion(video_id):
  obj = Get_frames(video_id=video_id)
  path = obj.get_frames()

  gather = GatherSimilarFaces(faces_path=path)
  gather.similar_face()
  gather.remove_rest()



  # make a dictionary of emotions
  emotions = {}
  path = path.replace('Frames', 'People_faces')
  total_Persons = os.listdir(path)
  for i in range(len(total_Persons)):
    new_path = path+'/'+total_Persons[i]
    name, emotion  = Analyze_pics(new_path)
    emotions[name] = emotion
  
  # remove utilized files
  # path = r'D:\Savior\fs\AI\face_emo_detection\data'
  path = ABSOLUTE_PATH + "/AI/face_emo_detection/data"
  shutil.rmtree(path, ignore_errors=True) # remove Frames
  
  # logic to get overall emotion of the video
  ''' 
  formula = sum of persons' emotions / total_Persons
  '''
  print("*****************\t",emotions)
  if 0 in emotions.values():
    print("******************\tAI didn't verify!")
    return 0 #"AI didn't verify!"
  else:
    result = sum(emotions.values())/len(emotions)
    if result >= 6:
      print("Seeker is in trouble", result)
      return int(result) # to get the percentage of all models
    else:
      print("Seeker is not in trouble", result)
      return 0 # 0 means Seeker is not in trouble

  


