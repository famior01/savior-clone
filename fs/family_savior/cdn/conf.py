import os 
from decouple import config


AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", cast=str)
AWS_STORAGE_BUCKET_NAME="savior-staticfiles"
AWS_S3_ENDPOINT_URL="https://sgp1.digitaloceanspaces.com"
AWS_SE_OBJECT_PARAMETERS={
  "CacheControl":"max-age=86400",
  "ACL":"public_read",
}

AWS_LOCATION="https://savior-staticfiles.sgp1.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE="family_savior.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE="family_savior.cdn.backends.StaticRootS3BotoStorage"


try:
  STATIC_ROOT = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'static')
except:
  STATIC_ROOT = '{}/{}/'.format(AWS_LOCATION, 'static')
STATIC_URL = 'static/'

try:
  MEDIA_ROOT = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'media')
except:
  MEDIA_ROOT = '{}/{}/'.format(AWS_LOCATION, 'media')
MEDIA_URL = 'media/'