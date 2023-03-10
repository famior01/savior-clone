from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
  myprofile,
  ProfileListView,
  ProfileDetailView,
  ProfileUpdateView,
  follow_unfollow_profile,
  FollowerListView,
  FollowingListView,
  IWatch_videos,
  Zakat_Posts,
  remove_follower,
  UserSearch,
  )

app_name = 'profiles'  # in case we need to use the namespace in the future
urlpatterns = [
  # all profiles list
  path('', login_required(ProfileListView.as_view()), name='all-profiles'),

  # show own profile
  path('myprofile/', myprofile, name='myprofile'), 
  path('update/<int:pk>', login_required(ProfileUpdateView.as_view()), name='profile-update'), 
  path('follow/', follow_unfollow_profile, name='follow-unfollow-profile'),

  # see Profiles
  path('<int:pk>/', login_required(ProfileDetailView.as_view()), name='profile-detail-view'),
  path('followers/<int:pk>/', login_required(FollowerListView.as_view()), name='followers'),
  path('following/<int:pk>/', login_required(FollowingListView.as_view()), name='following'),
  path('remove-follower/<int:pk>', remove_follower, name='remove-follower'),

  # Profile Posts
  path('iwatch/<int:pk>/', IWatch_videos ,name='iwatch'),
  path('Zakat_Posts/<int:pk>/', Zakat_Posts ,name='zakat_posts'),

  # Searching for Profiles
  path("search/", UserSearch.as_view(), name='search-user')
]
