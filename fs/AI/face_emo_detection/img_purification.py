'''
This function will remove all duplicate images from folder.
You need to provide path with either forward slash init or with -- r"path"
'''
import os
import filecmp
from glob import glob
from face_detection import Detection

class Purification:
    def __init__(self, fold_path):
        self.fold_path = fold_path
        
    def remove_duplicate_images(self):
        path = self.fold_path.replace("\\", '/') # to convert slashes
        faces_list = glob(path+'/*') 
        imgs_len = len(faces_list)
        
        remove_images=[]
        for img in range(len(faces_list)):
            nex_img = img+1
            while (nex_img < imgs_len):
                if faces_list[img]!= faces_list[nex_img]:
                    if filecmp.cmp(faces_list[nex_img], faces_list[img]):
                        # os.remove(faces_list[nex_img])
                        remove_images.append(faces_list[nex_img])
                nex_img+=1

        # now we got list: let's remove duplicates from this
        ls = set(remove_images)
        for i in ls:
            os.remove(i)
        print("All duplicated item have been removed")

    def purify_faces(self):
        det = Detection(mk_dir='faces2', 
        vid_frame_path=r'C:\Product\FS\Models\DEEPFACE\faces')
        # print(det.ls_of_frames)
        det.find_face()



if __name__ == "__main__":
    obj = Purification(r'C:\Product\FS\Models\DEEPFACE\faces')
    obj.remove_duplicate_images()
    # obj.purify_faces()
