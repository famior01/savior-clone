import os 

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME ="savior-staticfiles"
AWS_S3_ENDPOINT_URL="https://sgp1.digitaloceanspaces.com"
AWS_SE_OBJECT_PARAMETERS ={
  "CacheControl":"max-age=86400",
  "ACL":"public_read",
}
AWS_LOCATION="https://savior-staticfiles.sgp1.digitaloceanspaces.com"
DEFAULT_FILE_STORAGE="family_savior.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE="family_savior.cdn.backends.StaticRootS3BotoStorage"