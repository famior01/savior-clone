"""
It receives video ID, then get video and process it to get the result
Result involves: 
'bicycle'1, 'car'2, 'motorcycle'3, 'bird'14, 'cat'15, 'dog'16, 'horse'17, 'sheep'18, 'cow'19, 'umbrella'25, 'handbag'26, 'suitcase'28, 'pizza'53, 'cake'55, 'chair'56, 'couch'57,'potted plant'58, 'bed'59, 'dining table'60, 'toilet'61, 'tv'62, 'laptop'63, 'cell phone'67,'microwave'68, 'oven'69, 'toaster'70, 'sink'71, 'refrigerator'72, 'clock'74,'hair drier'78, 
Group-1: Curtain, Lampe, Celling-Fan, Chandelier, Stand-Fan, UPS 
Group-2: Generator, Sewing-Machine, Tabel, Washine-Machine, Wifi-Router 
Group-3: Iron, AC, Vacuum-Cleaner, Showcase, tablet, Wardrobe

--classes 1 2 3 14 15 16 17 18 19 25 26 28 53 55 56 57 58 59 60 61 62 63 67 68 69 70 71 72 74 78
"""

import os 
import sys
import subprocess
from glob import glob
from AI.face_emo_detection.get_frames import Get_frames
import moviepy.editor as mp
from zakat_posts.models import ZakatPosts
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
from decouple import config

ABSOLUTE_PATH = config('ABSOLUTE_PATH')

class Object_Detection:
  def __init__(self, id):
    self.id = id

  # getting video leng
  def get_length(self, filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        total_sec = int(float(result.stdout))
        return total_sec


  def mk_vid_short(self, id):
    ''' Here video will be made short, if it is less greater than 1 min, so that it will be easy to process '''
    print("\n************* In the video making process *************\n")
    print('****************\tID = ',id)
    F_or_V_path, v_fps = Get_frames(video_id=id, object_det=True).get_frames() 
    if v_fps=='small': #if not 1,  
      return 90 # show this message to user
    
    if v_fps=='Same': # if video lenght is less than 30, process full video
      return F_or_V_path
    
    if v_fps=='big':
      return 91 # show error message, that you have big house!

    # converting frames to video
    # frame ='D:/Savior/fs/AI/object_detection/data/Frames/1.jpg'
    frame = ABSOLUTE_PATH + "/AI/object_detection/data/Frames/1.jpg"
    img = cv2.imread(frame)
    height = img.shape[0]
    width = img.shape[1]   
    frameSize = (width, height)
    # path = 'D:/Savior/fs/AI/object_detection/sample.mp4'
    path = ABSOLUTE_PATH + "/AI/object_detection/sample.mp4"
    out = cv2.VideoWriter(path,cv2.VideoWriter_fourcc(*'mp4v'), v_fps, frameSize)
    print(f"*************\t{v_fps}\t*************")
    for filename in glob(F_or_V_path+'/*'):
        img = cv2.imread(filename)
        out.write(img)
    out.release()
    
    # deleting frames
    shutil.rmtree(F_or_V_path)
    return path
    
  def get_obj_file(self, video_path, models ):
    '''
    This function will create file, which will contain all the objects detected in the video
    '''
    print('\n************* In the object detection process *************\n')
    all_models = glob(models+'/*')
    # path = 'D:/Savior/fs/AI/object_detection/objects.txt' # declaring path
    path = ABSOLUTE_PATH + "/AI/object_detection/objects.txt" # declaring path
    with open(path, 'w') as f:
      for model in all_models:
        model = model.replace('\\', '/')
        print('\n******************', model, '******************')
        subpor_path = ABSOLUTE_PATH + "/AI/object_detection/yolov7/detect.py"
        subprocess.run(f'python {subpor_path} --weights {model} --conf-thres 0.75 --iou-thres 0.55 --img-size 640 --source {video_path}' , shell=True , stdout=f)
    f.close()
    
    # Delete run folder
    shutil.rmtree(f'{ABSOLUTE_PATH}/runs', ignore_errors=True)

    return path
  
  def get_objs(self, file_path):
    '''
    This function will create dictionary, which will contain all the objects detected in the video, with their count
    '''
    print('\n************* In the dataframe making process *************\n')
    # getting data from file 
    csv_fp = file_path.replace('.txt', '.csv')
    read_file = pd.read_csv(file_path)
    read_file.to_csv(csv_fp, index=None, header=True) 

    df = pd.read_csv(csv_fp)
    df = df[df.iloc[:,0].str.contains('sample.mp4')] 
    # print(df.head())
    try:
      df.iloc[:,0]=df.iloc[:,0].str.split(": ", expand = True)[1] # removing the usless file/paths with object name
    except Exception as e:
      print("******************", e, "******************")
      return e
    
    df = df[-df.iloc[:,0].str.startswith('Done')] # remove those which start with Done

    df = df.drop_duplicates() 
    df.fillna('', inplace=True) 
    # concatinate all columns with comma
    mdf = df.iloc[:,0]
    for i in range(1, len(df.columns)):
      mdf = mdf.str.cat(df.iloc[:,i],sep=",")

    mdf = mdf.str.split('Done.', expand=True)[0] # get object till Done
    mdf = mdf.drop_duplicates()
    mdf = mdf.str.strip()
    mdf = mdf.str.cat(sep=",")  # concatinate all rows with comma
    mdf = mdf.split(',') # split with comma
    mdf = [i for i in mdf if i] # remove empty strings

    # Here we are creating a dictionary with key as object and value as count, Here plural nouns is the last latest value 
    items = {}
    for i in range(len(mdf)):
      value = mdf[i][0:2].strip()
      key = mdf[i][2:].strip()
      items[key] = value

    return items

  def cal_prediction(self, result):
    '''
    Here, these are those objects which are commonly present in the Middle class family, so if we found any of these objects in the video, we will count them as 0, else we will count them as a particular number according to the percentage of its existance in the middel class family from 1-10. (1 means 10% and 10 means 100%)
    Then it will get percentage, Pass if and only if percentage is greater than 80% else Fail
    '''

    objects = {'couch':10, 'cat':3, 'suitcase':5, 'chair':8, 'potted plant':5, 'bed':10, 'dining table':5, 'toilet':1, 'tv':10, 'laptop':5, 'microwave':7, 'oven':6, 'sink':5, 'refrigerator':10, 'clock':5, "Curtain": 5, "Lampe": 1, "Celling-Fan": 1, "Chandelier": 1, "Stand-Fan": 1, "UPS": 1, "Generator": 1, "Sewing-Machine": 2, "Tabel": 5, "Washine-Machine": 10, "Wifi-Router": 1, "Iron": 5, "AC": 5, "Vacuum-Cleaner": 5, "Showcase": 8, "tablet": 1, "Wardrobe": 10}
    
    scores = []
    print("********** These Objects has been found!\t = ",result)
    if not result or len(result) <= 3: # if dictionary is empty or has one object, means wrong video has been uploaded
      return "Second video is not appropriate"
    else:
      for i in objects.keys():
        if i in result.keys(): # if family has object, assign 0
          scores.append(0)
        else:
          scores.append(objects[i])

      print(scores)
      per = int(sum(scores)/sum(objects.values())*100)
      if per >= 80:  # This family should not have almost 80% objects, which are found in the middle class family
        print('\n************ Object_det_per = ', per, '%*******************\n')
        return int(per) # to cal the percentage 
      else:
        print('\n*******************Zero from Object_det_per', per, '&*******************\n')
        return 0

  def engin(self):
    vid_path = self.mk_vid_short(self.id) # 4 frame at a sec
    # if video is less than 30 sec, return error to user
    if vid_path == 90:
      return "Video 2 should be longer than 10 sec!"
    elif vid_path == 91:
      return "Your Home is Big Masha-Allah, You don't need to get Help!"
    
    print("****************\t\tvideo path: ", vid_path)

    weight_path = ABSOLUTE_PATH + "/AI/object_detection/new_weights"
    # file_path = self.get_obj_file(video_path=vid_path, models='D:/Savior/fs/AI/object_detection/new_weights')
    file_path = self.get_obj_file(video_path=vid_path, models=weight_path)
    df = self.get_objs(file_path)
    prediction = self.cal_prediction(df)
    shutil.rmtree(f'{ABSOLUTE_PATH}/traced_model.pt', ignore_errors=True)
    return prediction
