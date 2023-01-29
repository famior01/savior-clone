'''
This class will make folder of similar images, and will purify all images
'''

from glob import glob
import os
import pandas as pd
from deepface import DeepFace
import shutil


class GatherSimilarFaces():
    def __init__(self, faces_path):
        self.faces_path = faces_path
        self.db_path = self.faces_path
        self.faces_list =  glob(self.db_path+'/*')
        self.imgs_len = len(self.faces_list)
        self.index = 0
        # create directory and save all directories over there 
        path = faces_path.replace('Frames', 'People_faces')
        print("\n****************\t Similar Face Gathering ****************\n")
        os.makedirs(path, exist_ok=True)
        os.chdir(path)


    def similar_face(self):
        '''
        this function will make folder of similar faces.
        '''
        # print("***********", self.faces_path, "***********")
        self.faces_list =  glob(self.db_path+'/*')
        print("\n********* len of frames_list", len(self.faces_list), " *********\n")


        try:
            df = DeepFace.find(img_path = self.faces_list[0],
                db_path = self.db_path,
                model_name = 'Facenet512', 
                model = DeepFace.build_model('Facenet512'),
                enforce_detection=False,
                detector_backend='retinaface'
                )
        except AttributeError or ValueError:
            pass
        else:
            # df is pandas dataframe
            similar_images_path = df['identity']
            os.makedirs('Person'+str(self.index), exist_ok=True)
            path = os.getcwd()
            path = path + '/Person'+str(self.index)
            for img_link in similar_images_path:
                try:
                    shutil.move(img_link, path)
                except FileNotFoundError or ValueError:
                    pass

            self.index+=1
            self.similar_face()
        
    def remove_rest(self):
        """
        This function will remove rest images from faces dir and will also remove those folder which are empty or have less then 5 images 
        """
        for img in self.faces_list: 
            os.remove(img)
        
        path = os.getcwd() 
        fold_len = len(os.listdir(path)) # total folder inside people face
        for i in range(fold_len):
            fold = 'Person'+str(i)
            no_files =len(os.listdir(fold))
            if no_files == 0 or no_files<3:
                shutil.rmtree(fold)
        print("Purified!")
    

# if __name__ == '__main__':
#     obj = GatherSimilarFaces(r'C:\Product\Savior\fs\AI\face_emo_detection\data\Frames')
#     obj.similar_face()
#     obj.remove_rest()
