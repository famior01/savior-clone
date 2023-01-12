from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.shortcuts import render
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from IWatch.models import IWatch
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
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse



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

@login_required
def IWatch_videos(request, pk):
  profile = Profile.objects.get(pk=pk)
  videos = IWatch.objects.filter(creator=profile).all()
  context = {
    'IWatch': True,
    'videos': videos,
    'profile': profile
  }
  return render(request, 'profiles/profile.html', context)

@login_required
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

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)
  #   view_profile = self.get_object()
  #   my_profile = Profile.objects.get(user=self.request.user)
  #   if view_profile.user in my_profile.following.all():
  #     context['following'] = True
  #   else:
  #     context['following'] = False
  #   return context

class FollowerListView(ListView):
  model = Profile
  template_name = 'profiles/followers.html'  

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    user = User.objects.get(pk=pk)
    return user

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.get_queryset()
    context['followers_profiles'] = Profile.objects.filter(following=user).all().exclude(user=user)
    context['view_profile'] = Profile.objects.get(user=user)
    return context


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

@login_required
def follow_unfollow_profile(request):
  if request.method == 'POST':
    user_to_toggle = request.POST.get('username')
    my_profile = Profile.objects.get(user=request.user)  
    pk = request.POST.get('profile_pk')
    print("******************\t\t = ",pk)
    obj = Profile.objects.get(pk=pk)
    data = {}
    if obj.user in my_profile.following.all():
      my_profile.following.remove(obj.user)
      data['status'] = 'Follow'
      return JsonResponse(data, safe=False)  

    else:
      my_profile.following.add(obj.user)
      recipient = User.objects.get(pk=pk) # notify following user I am following, follow back
      data['status'] = 'UnFollow'
      notify.send(request.user, recipient=recipient, verb="Started following you",description= True)
      return JsonResponse(data, safe=False)  

  return redirect('profiles:all-profiles')

@login_required
def remove_follower(request, pk):
  profile = Profile.objects.get(pk=pk)
  profile.following.remove(request.user)
  messages.success(request, f'{profile.user.full_name} will no longer be notified of your activities')
  return redirect(request.META.get('HTTP_REFERER'))


class ProfileListView(ListView):
  model = Profile
  template_name = 'profiles/profile_list.html'
  # context_object_name = 'profiles' # object_list*


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = User.objects.get(username__exact=self.request.user)
    my_profile = Profile.objects.get(user=user)
    context['profiles'] = Profile.objects.all().exclude(user=self.request.user)
    return context




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


class UserSearch(ListView):

  def get(self, request, *args, **kwargs):
    query = self.request.GET.get('query').strip()
    if query:
      profile_list = Profile.objects.filter(
        Q(user__username__contains=query) | Q(user__full_name__icontains=query)
      )    
      context = {
        'search_list': profile_list,
      }
      return render(request, "profiles/profile_list.html", context)
    else:
      return redirect(request.META.get('HTTP_REFERER'))
      


# class SendAllProfiles(ListView):
#   model = Profile
#   template_name = 'profiles/profile_list.html'
  
#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context['all_Profiles'] = json.dumps(list(Profile.objects.values()))
#       return context