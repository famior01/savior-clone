'''
This class will be used to get the cropped face area from images. Images have been gotten from video through get_frames.py file 
'''

from deepface import DeepFace
from glob import glob
from retinaface import RetinaFace
import os 
import matplotlib.pyplot as plt
import numpy as np
import cv2
from cv2 import dnn_superres

class Detection:
    def __init__(self, path, vid_frame_path, height=224, width=224):
        self.path= path
        self.frames = vid_frame_path
        self.index = 0
        self.no = 0
        self.height = height
        self.width = width
        self.ls_of_frames = glob(self.frames+'/*')  
        self.lol = len(self.ls_of_frames) # :)


    def make_dir(self):
        curr_dir = self.path.replace('Frames', 'Faces')
        os.makedirs(curr_dir, exist_ok=True)
        return curr_dir


    def find_face(self):
        # if no pic found it just passes
        faces = RetinaFace.extract_faces(
            img_path = self.ls_of_frames[self.index], align = False, allow_upscaling=True)
        
        path = self.make_dir()
        dim = (self.height, self.width)
        
        for f in faces:
            # Up-scaling 
            img = cv2.resize(f, dim)
            sr = dnn_superres.DnnSuperResImpl_create()
            model_path = r'fs\AI\face_emo_detection\FSRCNN_x4.pb'
            sr.readModel(model_path)
            sr.setModel("fsrcnn", 4) #x4
            result = sr.upsample(img)

            image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"{path}/{self.no}.png", image)
            self.no+=1 # unique pic 
        
        self.index+=1
        if self.index<self.lol:
            self.find_face()
        else:
            print("Done extracting faces")
    
    

if __name__ == "__main__":
    obj = Detection(path=r'C:\Product\FS_1.1\fs\AI\face_emo_detection\data\Frames',vid_frame_path=r'C:\Product\FS_1.1\fs\AI\face_emo_detection\data\Frames')
    obj.find_face()