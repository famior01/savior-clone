from deepface import DeepFace
from glob import glob
import pandas as pd
import os

def Analyze_pics(path):
        pictures = glob(path + '\*')
        information = {}
        angry = []
        disgust = []
        happy = []
        sad = []
        surprise = []
        neutral  = []
        gender = []
        age = []

        for i in pictures:
                Analysis = DeepFace.analyze(img_path =i, 
                detector_backend = 'retinaface',
                enforce_detection=False      
                )
                # print(Analysis)
                angry.append(Analysis['emotion']['angry'])
                disgust.append(Analysis['emotion']['disgust'])
                happy.append(Analysis['emotion']['happy'])
                sad.append(Analysis['emotion']['sad'])
                surprise.append(Analysis['emotion']['surprise'])
                neutral.append(Analysis['emotion']['neutral'])
                gender.append(Analysis['gender'])
                age.append(Analysis['age'])

        dic = {'Angry':angry, 'Disgust':disgust, 'Happy':happy, 'Sad':sad, 'Surprise':surprise, 'Neutral':neutral, 'Gender':gender, 'Age':age}
        df = pd.DataFrame(dic)
        # , df.Gender.mode()[1]
        return df.mean()



if __name__ == "__main__":
        path = r"C:\Product\FS_1.1\fs\AI\face_emo_detection\data\People_faces"
        total_Persons = os.listdir(path)
        for i in range(len(total_Persons)):
                result = Analyze_pics(path + "\\" + total_Persons[i])
                
                print('***************\n',total_Persons[i], "\n***************")
                print('\n***************\n\n',result, "\n***************\n")
                
