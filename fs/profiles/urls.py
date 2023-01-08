from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
  myprofile,
  invites_received_view,
  invite_profiles_list_view,
  ProfileListView,
  send_invitation,
  remove_from_following,
  accept_invitation,
  reject_invitation,
  ProfileDetailView,
  ProfileUpdateView,
  follow_unfollow_profile,
  FollowerListView,
  FollowingListView,
  IWatch,
  Zakat_Posts,
  remove_follower,
  )

app_name = 'profiles'  # in case we need to use the namespace in the future
urlpatterns = [
  # all profiles list
  path('', login_required(ProfileListView.as_view()), name='all-profiles'),
  path('send-invite/', send_invitation, name='send-invite'),
  path('remove-friend/', remove_from_following, name='remove-friend'),

  # show own profile
  path('myprofile/', myprofile, name='myprofile'),
  path('update/<int:pk>', login_required(ProfileUpdateView.as_view()), name='profile-update'), 
  path('follow/', follow_unfollow_profile, name='follow-unfollow-profile'),



  # show all those, whom I sent friend request
  path("sent-invites/", invite_profiles_list_view, name="sent-invites"),

  # function of my-invites
  path('my-invites/', invites_received_view, name='my-invites'),
  path('accept-invite/', accept_invitation, name='accept-invite'),
  path('reject-invite/', reject_invitation, name='reject-invite'),

  # see Profiles
  path('<int:pk>/', login_required(ProfileDetailView.as_view()), name='profile-detail-view'),
  path('followers/<int:pk>/', login_required(FollowerListView.as_view()), name='followers'),
  path('following/<int:pk>/', login_required(FollowingListView.as_view()), name='following'),
  path('remove-follower/<int:pk>', remove_follower, name='remove-follower'),

  # Profile Posts
  path('iwatch/<int:pk>/', IWatch ,name='iwatch'),
  path('Zakat_Posts/<int:pk>/', Zakat_Posts ,name='zakat_posts')
]
