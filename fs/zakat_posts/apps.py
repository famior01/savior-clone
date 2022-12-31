from django.apps import AppConfig


class ZakatPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zakat_posts'

    # this is the function that is called when the app is ready
    # this is where we import the signals.py file
    def ready(self):
        import zakat_posts.signals
