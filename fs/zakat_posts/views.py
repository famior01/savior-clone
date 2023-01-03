from django.shortcuts import render
from .models import ZakatPosts, ZakatPostsComment, UpVote, DownVote
from profiles.models import Profile
from django.shortcuts import render, redirect
from .forms import ZakatPostForm, ZakatPostsCommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from family_savior.settings import LOGIN_REDIRECT_URL
from django.contrib.auth.decorators import login_required
from posts.models import Posts
# from django.views.decorators.csrf import csrf_exempt
from AI.tasks import AI, notify_before_posting, notify_after_posting
import cv2
import os
from datetime import datetime, timedelta
import time
from django.contrib import messages
from notifications.signals import notify
from celery import shared_task
from celery import Celery

def create_zakat_posts(request):
  qs = ZakatPosts.objects.all()
  c_form = ZakatPostsCommentForm()
  profile = Profile.objects.all()
  form = ZakatPostForm(request.POST or None, request.FILES or None)
  # Initializing The forms 
  if request.method == 'POST':
    seeker = request.POST['seeker']
    print(seeker, "*******************\n")
    needed_money = request.POST['needed_money']
    print(needed_money, "*******************\n")
    video1 = request.POST['video1']
    print(video1, "********************\n")
    video2 = request.POST['video2']
    print(video2, "*******************\n")
    content = request.POST['content']
    profile = Profile.objects.get(user=request.user)
    
    # create object
    ZakatPosts.objects.create(creator=profile, seeker=seeker, needed_money=needed_money, video1=video1, video2=video2, content=content)
    
    # get object
    zp = ZakatPosts.objects.get(creator=profile, seeker=seeker, needed_money=needed_money, video1=video1, video2=video2)
    print(zp, "********** post **********\n")
    
    # update object
    profile.post_no += 1 # this will change each time
    zp.post_number = profile.post_no # on which number the post was created
    zp.save()
    profile.save()

    # #(=====================   AI   =====================)
    # ID = ZakatPosts.objects.filter(creator=profile, seeker=seeker, needed_money=needed_money, video1=video1, video2=video2).values('id')[0]['id']
    # print(id, '******** id *********')

    # print("\n************", ID, "************\n")
    # notify_before_posting.apply_async(args=[ID], ignore_result=False)
    # output = AI.apply_async(args=[ID], ignore_result=False)
    # notify_after_posting.apply_async(args=[ID], ignore_result=False)

    # output = output.get()

    # # for handling the error, which I made in the AI function
    # if type(output) == str: 
    #   notify.send(request.user, recipient=instance.creator.user, verb=output)
    #   zp = ZakatPosts.objects.get(id=ID) 
    #   zp.delete()

    # show this valid post to the user
    # zakat_posts = ZakatPosts.objects.values()
    # print(zakat_posts, "*****************")
    # zakat_posts_list = list(zakat_posts)
    # print(zakat_posts_list, "*****************")
    return JsonResponse({'status': 'save'})
  else:
    form = ZakatPostForm()
  context = {
    'form': form,
    'c_form': c_form,
    'qs': qs,
    'profile': profile
  }
  return render(request, 'zakat_posts/main.html', context)


@login_required
def create_comment(request):
  c_form = ZakatPostsCommentForm(request.POST or None)
  profile = Profile.objects.get(user=request.user)
  
  if request.method == 'POST':
    body = request.POST['body']
    post_id = request.POST['post_id']
    ZakatPostsComment.objects.create(user=profile, post=ZakatPosts.objects.get(id=post_id), body=body)
    print("\n\ndon with comment", body, post_id, profile, "*********\n\n")
    
    # print('Adding comment')
    # c_form = ZakatPostsCommentForm(request.POST)
    # if c_form.is_valid():
    #   instance = c_form.save(commit=False)
    #   instance.user = profile
    #   instance.post = ZakatPosts.objects.get(id=request.POST.get('post_id'))
    #   instance.save()

      # Notification Corner
    instance = ZakatPostsComment.objects.get(user=profile, post=ZakatPosts.objects.get(id=post_id), body=body)
    body = instance.body[:50] + '...' # to show only 50 characters in the notification
    if instance.user != instance.post.creator:
      notify.send(request.user, recipient=instance.post.creator.user, verb=body, action_object=instance.post, description=f'on post # {instance.post.post_number}')

    return JsonResponse({'status': 'save'})

  else:
    c_form = ZakatPostsCommentForm()
    context = {'c_form':c_form}
  return render(request, "zakat_posts/main.html", context=context)

@login_required
def upvote(request):
  '''
  This will handle the upvote, and will save it recordes in the database.
  'enable_upvote' = is for internal use, to save repitition of code
  post = is the Object of Post class declared in models.py
  '''
  if request.method == 'POST':
    def enable_upvote():
      upvote = UpVote.objects.create(user=user, post=post, upvoted=True)
      # upvote.save()
      post.upvote = post.upvote + 1
      post.save()

    post_id = request.POST.get('post_id')
    user= request.user
    print('################# ',post_id, '**************************')
    post = ZakatPosts.objects.get(id=post_id) # get the post object

    # check if the user has already upvoted the post
    upvote = UpVote.objects.filter(user=user, post=post, upvoted=True).first()
    if upvote != None: # if the user has already upvoted the post
      upvote.delete() # delete the upvote
      post.upvote = post.upvote - 1 
      post.save()
    
    else:
      # check if the user has already downvoted the post
      downvote = DownVote.objects.filter(user=user, post=post, downvoted=True).first()
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

@login_required
def downvote(request):
  
  if request.method == 'POST':
    def enable_downvote():
      # downvote the post
      downvote = DownVote.objects.create(user=user, post=post, downvoted=True)
      # downvote.save()
      post.downvote = post.downvote + 1
      post.save()
    
    post_id = request.POST.get('post_id')
    user= request.user
    post = ZakatPosts.objects.get(id=post_id)

    # check if the user has already downvoted the post
    downvote = DownVote.objects.filter(user=user, post=post, downvoted=True).first()
    if downvote != None:
      downvote.delete()
      post.downvote = post.downvote - 1
      post.save()
    else:
      # check if the user has already upvoted the post
      upvote = UpVote.objects.filter(user=user, post=post, upvoted=True).first()
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

@login_required
def satisfied(request):
  zp = ZakatPosts.objects.all()
  c_form = ZakatPostsCommentForm()
  profile = Profile.objects.get(user=request.user)

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
    'zp':zp,
    'c_form':c_form,
  }
  return render(request, 'zakat_posts/satisfied_vid.html', context=context)