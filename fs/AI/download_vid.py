import boto3

s3 = boto3.client('s3',
                  aws_access_key_id='DO00PEMMA4CX68BHFMMU',
                  aws_secret_access_key='Ue//eSthdoBzXZmTqrkH2zCsLGrT10dmHL0dM4NJrbE',
                  endpoint_url='https://sgp1.digitaloceanspaces.com')
bucket_name = 'savior-staticfiles'
key = 'media/zakat_video/mati_O.mp4'

s3.download_file(bucket_name, key, 'video.mp4')