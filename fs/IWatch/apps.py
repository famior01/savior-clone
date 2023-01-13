from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IWatch'

# this will change the title of the post in the admin panel     
    verbose_name = 'IWatch, Comments, Likes'