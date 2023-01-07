from .models import Profile, Relationship

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

#This will return the number of invitaions received by the other User
def invitaions_received_no(request):
  if request.user.is_authenticated:
    profile_obj = Profile.objects.get(user=request.user)
    qs_count = Relationship.objects.invitations_received(profile_obj).count()
    return {'invitations_no': qs_count} # will use this key to access
  return {}