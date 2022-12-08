'''
This function will get the frames from a video, you can specify the fps rate (after each second), but I have set it to 90sec. According to Harvard brain scientist Dr. Jill Bolte Taylor, ninety seconds is all it takes to identify an emotion and allow it to dissipate while you simply notice it. 

let's fix it with 20sec, and then we will see the result.
'''

from zakat_posts.models import ZakatPosts
# Imports 
import time
import sys
import os 
import cv2 
from zakat_posts.utils import playvideo

class Get_frames:
    def __init__(self, video_id=None, after_each_sec=20):
        self.vid_path = video_id
        self.second = after_each_sec

    def mk_dir(self):
        curr_dir = os.path.realpath(os.path.dirname(__file__))
        curr_dir = curr_dir+'\data\Frames'
        print("############\tCurrent Directory: ", curr_dir)
        os.makedirs(curr_dir, exist_ok=True)
        return curr_dir
    
    def get_frames(self):
        # here it will get video from our machine folder :(
        zak_post = ZakatPosts.objects.filter(id=self.vid_path).first()
        video1 = str(zak_post.video1.url)
        video1 = "C:/Product/FS_1.1/static_cdn" + video1
        video1 = video1.replace('/media/', '/media_root/')
        print('************', video1, '************')

        video = cv2.VideoCapture(str(video1))
        fps = video.get(cv2.CAP_PROP_FPS) 
        path = self.mk_dir()

        # to get frame of specific-sec
        frame_af_sec = fps*self.second 
        i=0 
        while(True):
            # want to get each frame after 1 second 
            frame_id = fps 
            # video will be set to e.g. 30sec 
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_id) 
            # read that frame, if not end
            ret, frame = video.read()
            # ret, when it reach to end, gets False
            if frame is not None:
                # write image on the current folder with frame id
                cv2.imwrite(f"{path}/{frame_id}.jpg", frame)
                i+=1
                fps+=frame_af_sec
                # time.sleep(5)
            
            else:
                print("*******ret == False********")
                break
                
        video.release()
        print("\n---------Done with Extracting Frames!---------\n")
        return path


# class Get_frames:
#     def __init__(self, video_path=None, yt_video_link=None, mk_dir_name='Frames', after_each_sec=1):
#         self.vid_path = video_path
#         self.mk_dir_name= mk_dir_name
#         self.second = after_each_sec
#         self.link = yt_video_link

#     def mk_dir(self):
#         curr_dir = os.getcwd()
#         _ = os.makedirs(str(self.mk_dir_name), exist_ok=True)
#         path = os.path.join(curr_dir, str(self.mk_dir_name)) 
#         return path
    
#     def get_frames(self):
#         # zak_post = ZakatPosts.objects.filter(video1=self.vid_path).first()
#         # video1 = zak_post.video1

#         if self.link != None:
#             url = str(self.link)
#             v = pafy.new(url)
#             best  = v.getbest(preftype='mp4')
#             # capture frames without downloading
#             video = cv2.VideoCapture(best.url)
#         else:
#             # Define the codec and create VideoWriter object
#             video = cv2.VideoCapture(str(self.vid_path))
#             # print(video, '**************************')

#         fps = video.get(cv2.CAP_PROP_FPS) 
#         path = self.mk_dir()

#         # to get frame of specific-sec
#         frame_af_sec = fps*self.second 
#         i=0 
#         while(video.isOpened()):
#             # want to get each frame after 1 second 
#             frame_id = fps 
#             print("*******Frame_id********")
#             # video will be set to e.g. 30sec 
#             video.set(cv2.CAP_PROP_POS_FRAMES, frame_id) 
#             print("*******video.set********")
#             # read that frame, if not end
#             ret, frame = video.read()
#             print("*******ret, frame********")
#             # ret, when it reach to end, gets False
#             if ret == False:
#                 print("*******ret == False********")
#                 break
#             else:
#                 # write image on the current folder with frame id
#                 cv2.imwrite(f"{path}/{frame_id}.jpg", frame)
#                 print("*******cv2.imwrite********")
#                 i+=1
#                 fps+=frame_af_sec

#             # time.sleep(5)
#         video.release()
#         print("\n---------Done with Extracting Frames!---------\n")


