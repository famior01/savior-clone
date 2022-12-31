from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    # # this is the function that is called when the app is ready
    # # this is where we import the signals.py file
    def ready(self):
        import profiles.signals
        