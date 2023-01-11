from django.shortcuts import render
from .models import IWatch, IWatchComment, Like, Dislike
from profiles.models import Profile
from django.shortcuts import render, redirect
from .forms import IWatchModelForm, CommentModelForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from family_savior.settings import LOGIN_REDIRECT_URL
from user.models import User
from django.contrib.auth.decorators import login_required
import random


class UploadVideoView(CreateView):
  model = IWatch
  form_class =  IWatchModelForm
  template_name = 'IWatch/upload.html'
  success_url = reverse_lazy('IWatch:Show-IWatch')


  # only author will be able to update the post
  def form_valid(self, form):
    profile = Profile.objects.get(user=self.request.user)
    form.instance.creator = profile

    if form.instance.creator == profile:
      return super().form_valid(form)
    else:
      form.add_error(None, "You are not authorized to update this post")
      return super().form_invalid(form)


class IWatchListView(ListView):
  model = IWatch
  template_name = 'IWatch/main.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      profile = Profile.objects.get(user=self.request.user)
      following_users = profile.following.all()
      following_profiles = Profile.objects.filter(user__in=following_users)
      following_profiles |= Profile.objects.filter(user=self.request.user)
      following_Videos = IWatch.objects.filter(creator__in=following_profiles)
      context['qs'] = following_Videos
      context['following_profiles'] = following_profiles
      return context

class IWatchDetailView(DetailView):
  model = IWatch
  template_name = 'IWatch/showIWatch.html'
  # context_object_name = 'IWatch'

  def get_object(self, *args, **kwargs):
    pk = self.kwargs.get('pk')
    iwatch = IWatch.objects.get(pk=pk)
    return iwatch
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['IWatch'] = self.get_object()
      items = list(IWatch.objects.all())
      # change 3 to how many random items you want
      random_objects = random.sample(items, 8)
      context['random_objects'] = random_objects
      context['seektime'] = 10
      return context
  


# @login_required(login_url=LOGIN_REDIRECT_URL)
# def post_comment_create_and_list_view(request):
#     # qs = IWatch.objects.all()
#     profile = Profile.objects.all()
    
#     # Initializing the form
#     p_form = IWatchModelForm()
#     c_form = CommentModelForm() 
#     post_added = False  # Flag to check if post is added or not
#     profile = Profile.objects.get(user=request.user)

#     if 'submit_p_form' in request.POST:
#       print('Adding post')
#       p_form = IWatchModelForm(request.POST, request.FILES)
#       if p_form.is_valid():
#         instance = p_form.save(commit=False)
#         instance.creator = profile  
#         instance.save()
#         p_form = IWatchModelForm()
#         post_added = True

#     # comment form
#     if 'submit_c_form' in request.POST:
#       print('Adding comment')
#       c_form = CommentModelForm(request.POST)
#       if c_form.is_valid():
#         instance = c_form.save(commit=False)
#         instance.user = profile
#         instance.post = IWatch.objects.get(id=request.POST.get('post_id'))
#         instance.save()
#         c_form = CommentModelForm()

#     # profile = Profile.objects.all()
#     # following_posts = Posts.objects.filter(author__in=following_profiles)
#     # just see those post which are postes by the user whom current user is following
#     # following_posts = Posts.objects.filter(author__in=profile.following.all())
    
#     # profile = Profile.objects.get(user=request.user)
    
#     profiles = Profile.objects.all()


#     context = {
#       'qs':following_posts,
#       'profiles':profiles,
#       'post_added':post_added,
#       'p_form':p_form,
#       'c_form':c_form,
#     }
#     return render(request, "IWatch/main.html", context=context)


@login_required(login_url=LOGIN_REDIRECT_URL)
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = IWatch.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
            like.delete()
        else:
            post_obj.liked.add(profile)
            like.value = 'Like'
            like.save()
        post_obj.save()

        

        # if not created:
        #     if like.value=='Like':
        #         like.value='Unlike'
        #     else:
        #         like.value='Like'
        # else:
        #     like.value='Like'

        #     post_obj.save()
        #     like.save()

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('IWatch:main-post-view')

def post_of_following_profiles(request):
    qs = IWatch.objects.all()
    
    context = {
      'qs':qs,
      'profile':profile,
      'following_posts':following_posts,
    }
    return render(request, "IWatch/main.html", context=context)

# delete post
# @login_required(login_url=LOGIN_REDIRECT_URL)
class PostDeleteView(DeleteView): 
    model = IWatch
    template_name = 'IWatch/confirm_delete.html'
    success_url = reverse_lazy('IWatch:main-post-view') # reverse_lazy is used to avoid circular import

    # only author will be able to delete the post
    def get_object(self, *args, **kwargs):
      pk = self.kwargs.get('pk')
      obj = IWatch.objects.get(pk=pk)
      if not obj.author.user == self.request.user:
        messages.warning(self.request, "You are not authorized to delete this post")
      return obj
    
# post update


class PostUpdateView(UpdateView):
    model = IWatch
    form_class = IWatchModelForm  # from forms.py
    template_name = 'IWatch/update.html'
    success_url = reverse_lazy('IWatch:main-post-view')

    # only author will be able to update the post
    def form_valid(self, form):
      profile = Profile.objects.get(user=self.request.user)
      if form.instance.author == profile:
        return super().form_valid(form)
      else:
        form.add_error(None, "You are not authorized to update this post")
        return super().form_invalid(form)



