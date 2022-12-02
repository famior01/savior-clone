from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'

# this will change the title of the post in the admin panel     
    verbose_name = 'Posts, Comments, Likes'