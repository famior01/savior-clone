"""
This functions works on DeepFace library. It will a Percentage (of being) of each emotions, corresponding to a particular person. then It will make DataFrame, then will give mean on it. Then it will convert that df to dictionary, then it will find larges percentage of emotion on that dic. and will return.

At the end I applied logic to get the number corresponding to the particular emotion!

In the engine it will get the average of all persons' emotion, and will return 1 (eligible) or 0 (ineligibel) if average > 6

"""

from deepface import DeepFace
from glob import glob
import pandas as pd
import os
import numpy as np
def Analyze_pics(path):
        pictures = glob(path + '/*')
        information = {}
        angry = [] 
        disgust = [] 
        happy = [] 
        sad = []  
        surprise = []
        neutral  = []
        # gender = []
        # age = []

        for i in pictures:
                Analysis = DeepFace.analyze(img_path = i, 
                detector_backend = 'retinaface',
                enforce_detection=False      
                )
                # print(Analysis)
                angry.append(Analysis[0]['emotion']['angry'])
                disgust.append(Analysis[0]['emotion']['disgust'])
                happy.append(Analysis[0]['emotion']['happy'])
                sad.append(Analysis[0]['emotion']['sad'])
                surprise.append(Analysis[0]['emotion']['surprise'])
                neutral.append(Analysis[0]['emotion']['neutral'])
                # gender.append(Analysis['gender'])
                # age.append(Analysis['age'])

                dic = {'Angry':angry, 'Disgust':disgust, 'Happy':happy, 'Sad':sad, 'Surprise':surprise, 'Neutral':neutral}
                df = pd.DataFrame(dic)
                # print(df)
                dictionary = dict(df.mean())
                max_emo = max(dictionary, key=dictionary.get)
                name = str(path.split('/')[-1])

                # Logic to calculate the emotion of single or multiple person
                
                if max_emo == "Sad":
                        max_emo = 10
                elif max_emo == "Angry":
                        max_emo = 10
                elif max_emo == "Disgust":
                        max_emo = 7
                elif max_emo == "Surprise":
                        max_emo = 6
                elif max_emo == "Neutral":
                        max_emo = 5
                else: # Happy
                        max_emo = 0

                return name, max_emo

# if __name__ == "__main__":

#         path = r"C:\Product\Savior\fs\AI\face_emo_detection\data\People_faces"
#         total_Persons = os.listdir(path)
#         for i in range(len(total_Persons)):
#                 name, emo = Analyze_pics(path + "\\" + total_Persons[i])
#                 # emo, name = Analyze_pics(path)
#                 print('\n---------------\n',emo, name, '\n---------------\n')


