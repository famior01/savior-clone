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


@login_required
def myprofile(request):
  zp = ZakatPosts.objects.all()
  profile = Profile.objects.get(user=request.user) #get curr user profile
  form = ProfileModelForm(request.POST or None, request.FILES or None ,instance=profile) # get curr user form to update

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
def invite_profiles_list_view(request):
  """ 
  Here we will all those profiles which have been sent friend request by the current user
  """
  user = request.user
  qs = Profile.objects.get_all_profiles_to_invite(user)
  
  context = {
    'qs': qs
  }
  return render(request, 'profiles/to-invite-list.html', context)

class ProfileListView(ListView):
  '''
  This will show all those profiles which are either friends or not friend of the current user
  '''
  model = Profile
  template_name = 'profiles/profile_list.html'
  # context_object_name = 'qs'

  def get_queryset(self):
    qs = Profile.objects.get_all_profiles(self.request.user)
    return qs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = User.objects.get(username__iexact=self.request.user)
    profile = Profile.objects.get(user=user)
    rel_r = Relationship.objects.filter(sender=profile)
    rel_s = Relationship.objects.filter(receiver=profile)
    rel_receiver = []
    rel_sender = []
    for item in rel_r:
        rel_receiver.append(item.receiver.user)
    for item in rel_s:
        rel_sender.append(item.sender.user)
    context["rel_receiver"] = rel_receiver
    context["rel_sender"] = rel_sender
    context['is_empty'] = False
    if len(self.get_queryset()) == 0:
        context['is_empty'] = True

    return context

@login_required
def send_invitation(request):
  '''Here we will receive Primary key of the user we want to send the friend request, and then we will create a relationship object'''

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
def remove_from_friends(request):
  '''Here we will receive Primary key of the user we want to remove from friends, and then we will delete the relationship object'''

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


# Accepting and rejecting friend requests all three 
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
  '''Here we will receive Primary key of the user we want to accept the friend request, and then we will update the relationship object'''

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
  '''Here we will receive Primary key of the user we want to reject the friend request, and then we will delete the relationship object'''

  if request.method == 'POST':
    pk = request.POST.get('profile_pk')
    sender = Profile.objects.get(pk=pk)
    receiver = Profile.objects.get(user=request.user)
    rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
    rel.delete()
  return redirect('profiles:my-invites')


# Profile detail view
class ProfileDetailView(DetailView):
  model = Profile
  template = 'profiles/detail.html'

  def get_object(self):
    user = self.kwargs.get('user')
    profile = Profile.objects.get(user=user)
    return profile # will return the profile object which we are currently looking at

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = User.objects.get(username__iexact=self.request.user)
    profile = Profile.objects.get(user=user)
    rel_r = Relationship.objects.filter(sender=profile)
    rel_s = Relationship.objects.filter(receiver=profile)
    rel_receiver = []
    rel_sender = []
    for item in rel_r:
        rel_receiver.append(item.receiver.user)
    for item in rel_s:
        rel_sender.append(item.sender.user)
    context["rel_receiver"] = rel_receiver
    context["rel_sender"] = rel_sender
    context['posts'] = self.get_object().get_all_authors_posts()
    context['len_posts'] = True if len(self.get_object().get_all_authors_posts())>0 else False
    return context


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