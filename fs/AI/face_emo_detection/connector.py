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

from .get_frames import Get_frames
# from .face_detection import Detection
from .find_similar_faces import GatherSimilarFaces
from .all import Analyze_pics
import os
import shutil


def find_emotion(video_id):
  obj = Get_frames(video_id=video_id)
  path = obj.get_frames()

  # det = Detection(path=path, vid_frame_path=path)
  # faces_path=det.find_face()

  gather = GatherSimilarFaces(faces_path=path)
  gather.similar_face()
  gather.remove_rest()

  emotions = {}
  path = path.replace('Frames', 'People_faces')
  total_Persons = os.listdir(path)
  for i in range(len(total_Persons)):
    name, emotion  = Analyze_pics(path + "\\" + total_Persons[i])
    emotions[name] = emotion
  
  path = r'C:\Product\FS_1.1\fs\AI\face_emo_detection\data'
  shutil.rmtree(path, ignore_errors=True) # remove Frames


  return emotions

