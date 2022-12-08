"""
Problem! you cannot directly use these model to this script, for this you need to make all dependencies to be loaded here!
"""



from glob import glob
import torch
import torch
from torchvision import models, transforms, datasets
from matplotlib import pyplot as plt
import  numpy as np
import cv2



class Detected_objs:
    def __init__(self, images_fold_path=None, models_path=None):
        self.models = models_path
        self.dic = {}
        self.path = images_fold_path
        self.p = self.path.replace("\\", '/') 
        self.images_list = glob(self.p+'/*')
        

    def detect(self, mod):
        # path = mod
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=mod, force_reload=True)
        # model = torch.load(mod)
        model_info = []
        for img in self.images_list:
            output = model(img)
            # some techniques to get Predicted values
            text1 = str(output).split('\n')[0]
            text2 = text1.split(' ')[3:]
            text3 = ' '.join(text2)
            text4 = text3.split(',')
            details = {}
            for i in range(len(text4)):
                text4[i] = text4[i].strip()
                # ls = text4[i].split(' ')
                details[text4[i].split(' ')[1]] = text4[i].split(' ')[0]
            # add all dic to the instance var
            model_info.append(details)
        return model_info

    def engine(self):
        path= self.models.replace("\\", '/') 
        model_lists = glob(path+'/*')
        for mod in model_lists:
            info = self.detect(mod)
            self.dic['model1'] = info
        return self.dic 


if __name__ == '__main__':
    obj = Detected_objs(images_fold_path=r'C:\Product\FS\Models\YOLO\frames', models_path = r'C:\Product\FS\Models\YOLO\models' )
    a = obj.engine()
    print(a)