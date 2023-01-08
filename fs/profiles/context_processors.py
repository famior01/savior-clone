from .models import Profile

def profile_picture(request):
  '''
  It will return the profile picture of the current logged in user
  '''
  if request.user.is_authenticated:
      user = request.user # for notifications
      profiles = Profile.objects.all()
      my_profile = Profile.objects.get(user=request.user) # for profile picture
      return {'profile_picture': my_profile.avatar.url, 'user': user, 'profiles': profiles, 'my_profile': my_profile}
  return {}

