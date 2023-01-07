from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
  myprofile,
  invites_received_view,
  invite_profiles_list_view,
  ProfileListView,
  send_invitation,
  remove_from_friends,
  accept_invitation,
  reject_invitation,
  ProfileDetailView,
  ProfileUpdateView,
  )

app_name = 'profiles'  # in case we need to use the namespace in the future
urlpatterns = [
  # all profiles list
  path('', login_required(ProfileListView.as_view()), name='all-profiles'),
  path('send-invite/', send_invitation, name='send-invite'),
  path('remove-friend/', remove_from_friends, name='remove-friend'),

  # show own profile
  path('myprofile/', myprofile, name='myprofile'),
  path('update/<int:pk>/', login_required(ProfileUpdateView.as_view()), name='profile-update'), 


  # show all those, whom I sent friend request
  path("sent-invites/", invite_profiles_list_view, name="sent-invites"),

  # function of my-invites
  path('my-invites/', invites_received_view, name='my-invites'),
  path('accept-invite/', accept_invitation, name='accept-invite'),
  path('reject-invite/', reject_invitation, name='reject-invite'),

  # see Profiles
  path('<user>/', login_required(ProfileDetailView.as_view()), name='profile-detail-view'),


]
