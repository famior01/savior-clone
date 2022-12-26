from django.shortcuts import render
from .models import ZakatPosts, ZakatPostsComment, UpVote, DownVote
from profiles.models import Profile
from django.shortcuts import render, redirect
from .forms import ZakatPostForm, ZakatPostsCommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from family_savior.settings import LOGIN_REDIRECT_URL
from django.contrib.auth.decorators import login_required
from posts.models import Posts
from AI.combination import AI
import cv2
import os
import time
# from .utils import playvideo


def zakatPosts_comment_create_and_list_view(request):
  qs = ZakatPosts.objects.all()
  profile = Profile.objects.all()

  # Initializing The forms
  p_form = ZakatPostForm()
  c_form = ZakatPostsCommentForm()
  post_added = False 

  profile = Profile.objects.get(user=request.user)

  if 'submit_p_form' in request.POST:
    # print('Adding post')
    p_form = ZakatPostForm(request.POST, request.FILES)
    if p_form.is_valid():
      # video1 = p_form.cleaned_data['video1']
      instance = p_form.save(commit=False)
      instance.creator= profile
      # Sending the video to the AI
      instance.save() # have to save it first, to get the id
      
      ID = instance.id
      print("\n************", ID, "************\n")
      output = AI(ID)

      # post_without_varification = True
      # if post_without_varification:
      #   instance.varified = False
      #   instance.save()
      #   post_added = True
      #   print("\n************", instance.varified, "************\n")
      
      if type(output) == str: # if output is a string
        print("\n************\t", output, "\t************\n")
        post_added = output
        time.sleep(5) # wait for 5 seconds, to show the error message
        instance.delete()

      elif type(output)!=str and output>0: # if output is 1
        print("\n************", output, "************\n")
        instance.varified = output
        instance.save()
        post_added = True
        print("\n************", instance.varified, "************\n")
      
      

      else: # if output is 0
        print("\n************", output, "************\n")
        instance.delete()
        post_added=False
        print("\n************\t Deleted object \t************\n")
        
    p_form = ZakatPostForm() # renew the form

  # comment form
  if 'submit_c_form' in request.POST:
    print('Adding comment')
    c_form = ZakatPostsCommentForm(request.POST)
    if c_form.is_valid():
      instance = c_form.save(commit=False)
      instance.user = profile
      instance.post = ZakatPosts.objects.get(id=request.POST.get('post_id'))
      instance.save()
      c_form = ZakatPostsCommentForm()


  context = {
    'qs':qs,
    'profile':profile,
    'post_added':post_added,
    'p_form':p_form,
    'c_form':c_form,
  }
  return render(request, "zakat_posts/main.html", context=context)

def upvote(request):
  '''
  This will handle the upvote, and will save it recordes in the database.
  'enable_upvote' = is for internal use, to save repitition of code
  post = is the Object of Post class declared in models.py
  '''
  if request.method == 'POST':
    def enable_upvote():
      upvote = UpVote.objects.create(user=user, post=post)
      upvote.save()
      post.upvote = post.upvote + 1
      post.save()

    post_id = request.POST.get('post_id')
    user= request.user
    print('################# ',post_id, '**************************')
    post = ZakatPosts.objects.get(id=post_id) # get the post object

    # check if the user has already upvoted the post
    upvote = UpVote.objects.filter(user=user, post=post).first()
    if upvote != None: # if the user has already upvoted the post
      upvote.delete() # delete the upvote
      post.upvote = post.upvote - 1 
      post.save()
    
    else:
      # check if the user has already downvoted the post
      downvote = DownVote.objects.filter(user=user, post=post).first()
      if downvote != None:
        downvote.delete()
        post.downvote = post.downvote - 1
        post.save()
        enable_upvote()
      else:
        # upvote the post
        enable_upvote()
    # data = {
    #       'value': like.value,
    #       'likes': post_obj.liked.all().count()
    #   }

    # return JsonResponse(data, safe=False)
  return redirect('zakat_posts:main-post-view')

def downvote(request):
  
  if request.method == 'POST':
    def enable_downvote():
      # downvote the post
      downvote = DownVote.objects.create(user=user, post=post)
      downvote.save()
      post.downvote = post.downvote + 1
      post.save()
    
    post_id = request.POST.get('post_id')
    user= request.user
    post = ZakatPosts.objects.get(id=post_id)

    # check if the user has already downvoted the post
    downvote = DownVote.objects.filter(user=user, post=post).first()
    if downvote != None:
      downvote.delete()
      post.downvote = post.downvote - 1
      post.save()
    else:
      # check if the user has already upvoted the post
      upvote = UpVote.objects.filter(user=user, post=post).first()
      if upvote != None:
        upvote.delete()
        post.upvote = post.upvote - 1
        enable_downvote()
      else:
        enable_downvote()
    
  return redirect('zakat_posts:main-post-view')

class PostDeleteView(DeleteView): 
    model = ZakatPosts
    template_name = 'zakat_posts/confirm_delete.html'
    success_url = reverse_lazy('zakat_posts:main-post-view') # reverse_lazy is used to avoid circular import

    # only author will be able to delete the post
    def get_object(self, *args, **kwargs):
      pk = self.kwargs.get('pk')
      obj = ZakatPosts.objects.get(pk=pk)
      if not obj.creator.user== self.request.user:
        messages.warning(self.request, "You are not authorized to delete this post")
      return obj


class PostUpdateView(UpdateView):
    model = ZakatPosts
    form_class = ZakatPostForm  # from forms.py
    template_name = 'zakat_posts/update.html'
    success_url = reverse_lazy('zakat_posts:main-post-view')

    # only author will be able to update the post
    def form_valid(self, form):
      profile = Profile.objects.get(user=self.request.user)
      if form.instance.creator == profile:
        return super().form_valid(form)
      else:
        form.add_error(None, "You are not authorized to update this post")
        return super().form_invalid(form)

def satisfied(request):
  return render(request, 'zakat_posts/satisfied_vid.html')