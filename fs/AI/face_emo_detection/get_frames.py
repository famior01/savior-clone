'''
This file will be used to get frames from video.
1. for face emotion detection
2. for object detection
Here are the parameters:
1. video_id: id of video from zakat_posts
2. after_each_sec: after how many seconds you want to get frame
3. object_det: if you want to get frames for object detection, then set it to True

it will create a folder name data/Frames, and will save all frames in it. and will save this folder to respective location.
'''

from zakat_posts.models import ZakatPosts
# Imports 
import time
import sys
import os 
import cv2 
import subprocess
import shutil
class Get_frames:
    def __init__(self, video_id=None, object_det=False):
        self.vid_path = video_id
        self.fps = 0.5 # 50 % frames!
        self.object_det = object_det

    # Get Length of video
    def get_length(self, filename):
        print('************', filename, '**********filename**')
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        print('************', result.stdout, '*******stdout*****')
        total_sec = int(float(result.stdout))
        return total_sec

        
    def mk_dir(self):
        if self.object_det:
            curr_dir = r'C:/Product/Savior/fs/AI/object_detection'
        else:
            curr_dir = os.path.realpath(os.path.dirname(__file__)) # for finding the curr dir
        curr_dir = curr_dir+'/data/Frames'
        os.makedirs(curr_dir, exist_ok=True)
        return curr_dir
    
    def get_frames(self):
        # here it will get video from our machine folder :(
        zak_post = ZakatPosts.objects.filter(id=self.vid_path).first()
        if self.object_det:
            try: # if video2 is not given then it will give error
                video = str(zak_post.video2.url)
            except ValueError:
                return 'video2'
        else:
            try: # if video1 is not given then it will give error
                video = str(zak_post.video1.url)
            except ValueError:
                return 'video1'
            
        video = "C:/Product/Savior/fs/" + video
        # video = video.replace('/media/', '/media_root/')
        print('************', video, '******video******')
        
        # if video reached to its limit then break it!
        length_of_video = self.get_length(video)
    
        """
        I want to manage the size of video, to get stuff faster!
        Here Suppose the video of 24 fps, and I need to get frames with respect to fps and length of video

        if I reduce Percentage, No of Frames should decrease, (FPS X PERCENTAGE X LENGTH OF VID) and no of jumps btw frames should be large to complete all frames in the given time(FPS X (1-PERCENTAGE)). 
            ## 0.1 Means get only 10 % Frames, by increasing the jumps
        
        if I increase Percentage, No of Frames should increase, (FPS X PERCENTAGE X LENGTH OF VID) and no jump btw frames should be small to complete all frames in the given time(FPS X (1-PERCENTAGE)).
            ## 0.9 Means get 90 % Frames, by decreasing the jumps

        here regardless of (i<total_frames) condition on while, it finishes all frames before this!, if wanna get exact no of frames, then you need to fixe the jump!, (but I guess it is fine, and working good) 
        """

        if self.object_det and length_of_video <10: 
            self.fps='small'
            return 0,  self.fps # He didn't proper video, show error
        elif self.object_det and length_of_video <20: 
            self.fps = "Same" # maybe he made in a hurry, so we will pass whole
            return video, self.fps
            print("***********", self.fps, "***********")
        elif self.object_det and length_of_video <30:
            self.fps = 0.95 # get 90% of frames
            print("*************", self.fps, "*************")
        elif self.object_det and length_of_video <60:
            self.fps = 0.90 # get 85% of frames
            print("*************", self.fps, "*************")
        elif self.object_det and length_of_video <90:
            self.fps = 0.85
            print("*************", self.fps, "*************")
        elif self.object_det and length_of_video <120:
            self.fps = 0.80
            print("*************", self.fps, "*************")
        
        elif self.object_det and length_of_video <150:
            self.fps = 0.75
            print("*************", self.fps, "*************")

        elif self.object_det and length_of_video >150: # 2.5 minutes
            self.fps = 'big'
            return 0, self.fps
        else: # for both face_ana
            self.fps = 0.50 # else get 50% of frames,
            print("*************", self.fps, "*************")

        print("\n\tLength of video is: ", length_of_video, "seconds")

        video = cv2.VideoCapture(video) # str
        v_fps = video.get(cv2.CAP_PROP_FPS) 
        path = self.mk_dir()
        
        # to get frame of specific-sec
        total_frames = int(length_of_video*self.fps*v_fps)
        Frame_no = int(v_fps*(1-self.fps)) # frame no out of all frames 24 X 0.95 = 22
        
        print(v_fps, "= Video FPS ***********************")
        print(total_frames, "= Total Frames ***********************")
        print(Frame_no, "= frame Number ***********************")
        
        i=0 
        jump_frame = Frame_no # jump with same difference, according to fps x percentage
        while(i!=total_frames):
            # video getting frame id, and will get additionals frame 
            video.set(cv2.CAP_PROP_POS_FRAMES, jump_frame) 
            # read that frame, if not end
            ret, frame = video.read()
            # ret, when it reach to end, gets False
            if frame is not None:
                # write image on the current folder with frame id
                cv2.imwrite(f"{path}/{i}.jpg", frame)
                i+=1
                jump_frame+=Frame_no
            else:
                break

        print("\nTotal Frames Made ********** \t= ", i)
        print("last frame id ********** \t= ", jump_frame)
        video.release()
        print("\n---------Done with Extracting Frames!---------\n")
        if self.object_det:
            # if old fps = 26, for making short video, v_fps*self.fps = 22
            return path, int(v_fps*self.fps) 
            print("***********", path,"\t", v_fps,"***********")
        else:
            return  path


#TODO;
# Problem, if you give vertical video(9:16), then it flip that video and then make short video, which is usless for YOLOV