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
# Create your views here.

def zakatPosts_comment_create_and_list_view(request):
  qs = ZakatPosts.objects.all()
  profile = Profile.objects.all()

  # Initializing The forms
  p_form = ZakatPostForm()
  c_form = ZakatPostsCommentForm()
  post_added = False 

  profile = Profile.objects.get(user=request.user)

  if 'submit_p_form' in request.POST:
    print('Adding post')
    p_form = ZakatPostForm(request.POST, request.FILES)
    if p_form.is_valid():
      instance = p_form.save(commit=False)
      instance.creator= profile
      instance.save()
      p_form = ZakatPostForm()
      post_added = True

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

