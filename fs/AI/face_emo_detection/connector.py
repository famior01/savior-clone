from .get_frames import Get_frames
from .face_detection import Detection
from .find_similar_faces import GatherSimilarFaces
from .all import Analyze_pics
import os

def find_emotion(video_id):
  obj = Get_frames(video_id=video_id)
  path = obj.get_frames()

  # det = Detection(path=path, vid_frame_path=path)
  # det.find_face()

  gather = GatherSimilarFaces(faces_path=path)
  gather.similar_face()
  gather.remove_rest()

  path = path.replace('Frames', 'People_faces')
  total_Persons = os.listdir(path)
  for i in range(len(total_Persons)):
    result = Analyze_pics(path + "\\" + total_Persons[i])
    print('\n***************\n',result, "\n***************\n")



"""
#TODO:
Now you need to find the best fps no of frames to be extracted from the video, else it won't work properly. Do experiment with other videos and find the best fps according to the length of the video. make algorithms!
"""