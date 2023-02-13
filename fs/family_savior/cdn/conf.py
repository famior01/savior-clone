import os 
from decouple import config


AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME="savior-staticfiles"
AWS_S3_ENDPOINT_URL="https://sgp1.digitaloceanspaces.com"

AWS_SE_OBJECT_PARAMETERS={
  "CacheControl":"max-age=86400",
  "ACL":"public_read",
}
# AWS_LOCATION="https://savior-staticfiles.sgp1.digitaloceanspaces.com"


DEFAULT_FILE_STORAGE="family_savior.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE="family_savior.cdn.backends.StaticRootS3BotoStorage"



# Use AWS_S3_ENDPOINT_URL here if you haven't enabled the CDN and got a custom domain. 
STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/static/'
STATIC_ROOT = 'static/'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/media/'
MEDIA_ROOT = 'media/'

# try:
#   STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'static')
# except:
#   STATIC_URL = '{}/{}/'.format(AWS_LOCATION, 'static')

# STATIC_ROOT = 'static/'

# try:
#   MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'media')
# except:
#   MEDIA_URL = '{}/{}/'.format(AWS_LOCATION, 'media')

# MEDIA_ROOT = 'media/'