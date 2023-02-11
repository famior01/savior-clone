from .models import Profile
from decouple import config

Production=config('USE_PRODUCTION', default=False, cast=bool)

def profile_picture(request):
  '''
  It will return the profile picture of the current logged in user
  '''
  if request.user.is_authenticated:
      user = request.user # for notifications
      profiles = Profile.objects.all()
      my_profile = Profile.objects.get(user=request.user) # for profile picture
      return {'profile_picture': my_profile.picture.url, 'user': user, 'profiles': profiles, 'my_profile': my_profile, 'Production': Production}
  return {}

