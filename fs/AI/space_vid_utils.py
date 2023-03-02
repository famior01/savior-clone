import boto3
from botocore.client import Config
import os 
import cv2
import subprocess
import shutil
import tempfile
from decouple import config
ABSOLUTE_PATH = config('ABSOLUTE_PATH')


def get_space_vid_len(path):
    """
    I have tried manay ways to get the video length from digital ocean space, only this mathod is working, It will not work with local machine!, It also takes some time to get the video length 
    """
    path = path.replace("/media/", "media/")
    session = boto3.Session(
        aws_access_key_id='DO00XDV6B46BWBWW4GQV',
        aws_secret_access_key='f2h5A3dPzsskKcxAKmBe5bP16fgwnsoC1wyoBl58K1g',
    )

    # Generate a signed URL for your file
    s3 = session.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com')
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'savior-space', 'Key': path},
        ExpiresIn=3600,  # The URL will be valid for 1 hour
    )

    # download the video to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.mp4') as tmp_file:
        s3.download_file('savior-space', path, tmp_file.name)

        # read the video using cv2.VideoCapture()
        cap = cv2.VideoCapture(tmp_file.name)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_sec = total_frames/fps
        return total_sec


def delete_vid_from_bucket(url):
    url = url.replace("/media/", "media/")
    s3 = boto3.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com', aws_access_key_id='DO00XDV6B46BWBWW4GQV', aws_secret_access_key='f2h5A3dPzsskKcxAKmBe5bP16fgwnsoC1wyoBl58K1g', config=Config(signature_version='s3v4'))
    s3.delete_object(Bucket='savior-space', Key=url)


def get_audio_of_space_vid(path):
    """
    It will download audio of given video from space and save it in AI folder
    """
    path = path.replace("/media/", "media/")
    session = boto3.Session(
        aws_access_key_id='DO00XDV6B46BWBWW4GQV',
        aws_secret_access_key='f2h5A3dPzsskKcxAKmBe5bP16fgwnsoC1wyoBl58K1g',
    )

    # Generate a signed URL for your file
    s3 = session.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com')
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'savior-space', 'Key': path},
        ExpiresIn=3600,  # The URL will be valid for 1 hour
    )

    # download the video to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.mp4') as tmp_file:
        s3.download_file('savior-space', path, tmp_file.name)

        video = me.VideoFileClip(tmp_file.name)
        audio = video.audio
        if audio == None: # if no audio in video 
            return "Number first video has no audio"
        else:
            audio.write_audiofile(ABSOLUTE_PATH+'/AI/sentiment_ana/sample.mp3')


def download_space_vid(path, destination):
    """
    It will download audio of given video from space and save it in AI folder
    """
    path = path.replace("/media/", "media/")
    s3 = boto3.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com', aws_access_key_id='DO00XDV6B46BWBWW4GQV', aws_secret_access_key='f2h5A3dPzsskKcxAKmBe5bP16fgwnsoC1wyoBl58K1g', config=Config(signature_version='s3v4'))

    s3.download_file('savior-space', path, destination)
    return str(destination)

