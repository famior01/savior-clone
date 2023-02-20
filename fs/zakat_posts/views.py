from django.shortcuts import render
from .models import ZakatPosts, ZakatPostsComment, UpVote, DownVote
from profiles.models import Profile
from django.shortcuts import render, redirect
from .forms import ZakatPostForm, ZakatPostsCommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from IWatch.models import IWatch
from AI.tasks import AI#, notify_before_posting #, notify_after_posting
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
  profile = Profile.objects.get(user=request.user)
  p_form = ZakatPostForm(request.POST or None, request.FILES or None)
  # Initializing The forms 
  if 'submit_p_form' in request.POST:
    p_form = ZakatPostForm(request.POST, request.FILES)    
    if p_form.is_valid():
      instance = p_form.save(commit=False)
      instance.creator= profile
      instance.save() # have to save it first, to get the 
      profile.post_no += 1 # this will change each time
      zp = ZakatPosts.objects.get(id=instance.id)
      zp.post_number = profile.post_no # on which number the post was created
      zp.save()
      notify.send(request.user, recipient=request.user, verb='afte form is valid ')
      profile.save()
      print('in the Zakat posts view.py **********\n\n')
      #(=====================   AI   =====================)
      # ID = instance.id
      ID = zp.id
      print("\n************", ID, "************\n")
      notify.send(request.user, recipient=request.user, verb=f'the ID is {ID}, after getting id')
      # notify_before_posting.apply_async(args=[ID])
      notify.send(request.user, recipient=request.user, verb=f'Abdullah (AI) is checking your post which might takes more than an hour, after evaluation you will be notified with status of your post. Please wait!')

      output = AI.delay(ID)
      # notify_after_posting.apply_async(args=[ID], ignore_result=False)
      notify.send(request.user, recipient=request.user, verb=f'after getting {output} = output')
      print("***********", output, "**output*********")
      output = output.get() 

      # if didn't varify, then save in db, and don't show, and minus the post number
      if type(output) == int and output<50:
        profile.post_no -= 1 

      # for handling the error, which I made in the AI function
      if type(output) == str: 
        '''Not saving posts, because the AI function returned an error'''
        notify.send(request.user, recipient=instance.creator.user, verb=output)
        zp = ZakatPosts.objects.get(id=ID)
        profile.post_no -= 1 # this will change each time
        zp.delete()
      
    p_form = ZakatPostForm() # renew the form
  
  context = {
    'p_form': p_form,
    'qs': qs,
    'my_profile': profile
  }

  return render(request, 'zakat_posts/main.html', context)

@login_required
def paid_money(request):
  if request.method == 'POST':
    post_id = request.POST['post_id']
    amount = request.POST['amount'] 
    print("*********** post_id", post_id, "***********")
    print("*********** amount", amount, "***********")
    profile = Profile.objects.get(user=request.user)
    zp = ZakatPosts.objects.get(id=post_id)
    if amount: # if the amount is not 0
      zp.paid += int(amount)
      zp.donor.add(profile)
      if zp.paid >= zp.needed_money:
        zp.satisfied = True
      zp.save()
      messages.success(request, f'You have paid {amount} to {zp.seeker}, Thank you for your generosity!')
      notify.send(request.user, recipient=zp.creator.user, verb=f'{profile.user.full_name} have paid {amount} to {zp.seeker}, You should info seeker about this payment.')
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      messages.error(request, f'You have paid nothing :)')
      return redirect(request.META.get('HTTP_REFERER'))
  return redirect(request.META.get('HTTP_REFERER'))

@login_required
def create_comment(request):
  # c_form = ZakatPostsCommentForm(request.POST or None)
  profile = Profile.objects.get(user=request.user)
  qs = ZakatPosts.objects.all()
  form = ZakatPostForm()
  
  if request.method == 'POST':
    body = request.POST["body"]
    post_id = request.POST['post_id']

    zpc = ZakatPostsComment(user=profile, post=ZakatPosts.objects.get(id=post_id), body=body)
    zpc.save()
  
    # Notification Corner
    body = zpc.body[:50] + '...' # to show only 50 characters in the notification
    if zpc.user != zpc.post.creator:
      notify.send(request.user, recipient=zpc.post.creator.user, verb=body, action_object=zpc.post, description=f'on post # {zpc.post.post_number}')

    comments = ZakatPostsComment.objects.filter(post=zpc.post).values()
    list_of_comments = list(comments)
    no_of_comments = ZakatPostsComment.objects.filter(post=post_id).count()
    c_user = zpc.user.user.username
    c_body = zpc.body
    c_date = zpc.created_at
    data = {
      'status': 'save',
      'c_user': c_user,
      'c_body': c_body,
      'c_date': c_date,
      'no_of_comments': no_of_comments,
      'list_of_comments': list_of_comments,
    }
    return JsonResponse(data, safe=False)

  context = {
    # 'c_form': c_form,
    'qs': qs,
    'profile': profile
  }
  return render(request, "zakat_posts/main.html", context)

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

    post_id = request.POST['post_id']
    user= request.user
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
        enable_upvote()

      data = {
        'upvote': post.upvote,
      }
      return JsonResponse(data, safe=False)
    
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
    
    post_id = request.POST['post_id']
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

      data = {
        'downvote': post.downvote,
      }
      return JsonResponse(data, safe=False)
    
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