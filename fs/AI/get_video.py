# import boto3
# from botocore.client import Config
# from decouple import config
# import os 

# def get_vid_from_bucket(url):
#     print("*************", url,"*********")
#     video_path = 'media/' + url
#     # Initialize the client with your API key and secret key
#     session = boto3.Session(
#         aws_access_key_id=config("AWS_ACCESS_KEY_ID", cast=str),
#         aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY", cast=str)
#     )

#     # Generate a signed URL for your file
#     s3 = session.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com', config=Config(signature_version='s3v4'))
#     url = s3.generate_presigned_url(
#         'get_object',
#         Params={'Bucket': 'savior-staticfiles', 'Key': video_path},
#         ExpiresIn=7200,  # The URL will be valid for 2 hour
#     )
#     return url