from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Relationship
from django.shortcuts import render
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from posts.models import Posts
from zakat_posts.models import ZakatPosts
from django.contrib.auth.decorators import login_required
from .forms import ProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from family_savior.settings import AUTH_USER_MODEL
from user.models import User
from django.contrib.auth import get_user_model
from notifications.signals import notify
from django.contrib import messages



@login_required
def myprofile(request):
  # zp = ZakatPosts.objects.all()
  profile = Profile.objects.get(user=request.user) #get curr user profile
  form = ProfileModelForm(request.POST or None, request.FILES or None ,instance=profile) # get 
  zp = profile.get_zakat_posts() 

  confirm = False
  if request.method == "POST":
    if form.is_valid():
      form.save()
      confirm = True
  
  context = {
    'profile': profile,
    'form': form,
    'confirm': confirm,
    'zp': zp
  }
  return render(request, 'profiles/profile.html', context)


def IWatch(request, pk):
  profile = Profile.objects.get(pk=pk)
  posts = Posts.objects.filter(author=profile).all()
  context = {
    'IWatch': True,
    'posts': posts,
    'profile': profile
  }
  return render(request, 'profiles/profile.html', context)

# Profile list view
def Zakat_Posts(request, pk):
  profile = Profile.objects.get(pk=pk)
  zp = ZakatPosts.objects.filter(creator=profile).all()
  context = {
    'ZakatPosts': True,
    'profile': profile,
    'zp': zp
  }
  return render(request, 'profiles/profile.html', context)
  


# Profile detail view
class ProfileDetailView(DetailView):
  model = Profile
  template_name = 'profiles/profile.html'
  # context_object_name = 'profile'

  def get_object(self):
    pk = self.kwargs.get('pk')
    view_profile = Profile.objects.get(pk=pk)
    return view_profile 

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    view_profile = self.get_object()
    my_profile = Profile.objects.get(user=self.request.user)
    if view_profile.user in my_profile.following.all():
      context['following'] = True
    else:
      context['following'] = False
    return context

class FollowerListView(ListView):
  model = Profile
  template_name = 'profiles/followers.html'
  context_object_name = 'profiles'

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    user = User.objects.get(pk=pk)
    # view_profile = Profile.objects.get(pk=pk)
    followers_profiles = Profile.objects.filter(following=user).all().exclude(user=user)
    return followers_profiles

class FollowingListView(ListView):
  model = Profile
  template_name = 'profiles/following.html'
  context_object_name = 'profiles'

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    all_users = profile.get_following()
    following_profiles = Profile.objects.filter(user__in=all_users).all().exclude(user=user)
    return following_profiles

def follow_unfollow_profile(request):
  if request.method == 'POST':
    user_to_toggle = request.POST.get('username')
    my_profile = Profile.objects.get(user=request.user)  
    pk = request.POST.get('profile_pk')
    obj = Profile.objects.get(pk=pk)

    if obj.user in my_profile.following.all():
      my_profile.following.remove(obj.user)
    else:
      my_profile.following.add(obj.user)
      recipient = User.objects.get(pk=pk) # notify following user I am following, follow back
      notify.send(request.user, recipient=recipient, verb="Started following you",description= True)
    return redirect(request.META.get('HTTP_REFERER'))
    
  return redirect('profiles:all-profiles')

# Remove me from follower following list
def remove_follower(request, pk):
  profile = Profile.objects.get(pk=pk)
  profile.following.remove(request.user)
  messages.success(request, f'{profile.user.full_name} will no longer be notified of your activities')
  return redirect(request.META.get('HTTP_REFERER'))

@login_required
def invite_profiles_list_view(request):
  """ 
  Here we will all those profiles which have been sent following request by the current user
  """
  user = request.user
  qs = Profile.objects.get_all_profiles_to_invite(user)
  
  context = {
    'qs': qs
  }
  return render(request, 'profiles/to-invite-list.html', context)

class ProfileListView(ListView):
  '''
  This will show all those profiles which are either following or not following of the current user
  '''
  model = Profile
  template_name = 'profiles/profile_list.html'
  context_object_name = 'profiles' # object_list*

  def get_queryset(self):
    qs = Profile.objects.get_all_profiles(self.request.user)
    return qs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = User.objects.get(username__iexact=self.request.user)
    myprofile = Profile.objects.get(user=user)
    
    # following profiles 
    following_user = user.profile.get_following()
    following_profiles= Profile.objects.filter(user__in=following_user)
    context['following_profiles'] = following_profiles 

    # followers profiles
    followers = Profile.objects.filter(following=user).all()
    context['followers'] = followers
    return context

@login_required
def send_invitation(request):
  '''Here we will receive Primary key of the user we want to send the following request, and then we will create a relationship object'''

  if request.method == 'POST':
    pk = request.POST.get('profile_pk')
    user = request.user
    sender = Profile.objects.get(user=user)
    receiver = Profile.objects.get(pk=pk)
    rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
    rel.save()
    return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect('profiles:all-profiles')

@login_required
def remove_from_following(request):
  '''Here we will receive Primary key of the user we want to remove from following, and then we will delete the relationship object'''

  if request.method == 'POST':
    pk = request.POST.get('profile_pk')
    user = request.user
    sender = Profile.objects.get(user=user)
    receiver = Profile.objects.get(pk=pk)
    rel = Relationship.objects.get(
      (Q(sender=sender) & Q(receiver=receiver)) |
      (Q(sender=receiver) & Q(receiver=sender)))
    rel.delete()
    return redirect(request.META.get('HTTP_REFERER'))
  
  return redirect('profiles:all-profiles')


# Accepting and rejecting following requests all three 
@login_required
def invites_received_view(request):
  profile = Profile.objects.get(user=request.user)
  qs = Relationship.objects.invitations_received(profile)
  results = list(map(lambda x: x.sender, qs))
  is_empty = False
  if len(results) == 0:
      is_empty = True

  context = {
      'qs': results,
      'is_empty': is_empty,
  }

  return render(request, 'profiles/my-invites.html', context)

@login_required
def accept_invitation(request):
  '''Here we will receive Primary key of the user we want to accept the following request, and then we will update the relationship object'''

  if request.method == 'POST':
    pk = request.POST.get('profile_pk')
    sender = Profile.objects.get(pk=pk)
    receiver = Profile.objects.get(user=request.user)
    rel = get_object_or_404(Relationship,sender=sender, receiver=receiver)
    if rel.status == 'send':
      rel.status = 'accepted'
      rel.save()

  return redirect('profiles:my-invites')

@login_required
def reject_invitation(request):
  '''Here we will receive Primary key of the user we want to reject the following request, and then we will delete the relationship object'''

  if request.method == 'POST':
    pk = request.POST.get('profile_pk')
    sender = Profile.objects.get(pk=pk)
    receiver = Profile.objects.get(user=request.user)
    rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
    rel.delete()
  return redirect('profiles:my-invites')



# update profile model, class base view
class ProfileUpdateView(UpdateView):
  model = Profile
  form_class = ProfileModelForm  # from forms.py
  template_name = 'profiles/update.html'
  success_url = '/profiles/myprofile/'

  # only author will be able to update the post
  def form_valid(self, form):
    profile = Profile.objects.get(user=self.request.user)

    if form.instance.user == profile.user:
      return super().form_valid(form)
    else:
      form.add_error(None, "You are not authorized to update this post")
      return super().form_invalid(form)