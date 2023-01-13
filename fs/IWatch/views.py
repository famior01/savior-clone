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
from notifications.signals import notify
from django.db.models import Q
from hitcount.views import HitCountDetailView

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


#TODO; Recommendation system
#TODO; solve the bug of video skeetime


#  I need hitcoutn herer
class IWatchDetailView(HitCountDetailView):
  model = IWatch
  template_name = 'IWatch/showIWatch.html'
  count_hit = True

  # context_object_name = 'IWatch'

  def get_object(self, *args, **kwargs):
    pk = self.kwargs.get('pk')
    iwatch = IWatch.objects.get(pk=pk)
    return iwatch
  
  def get_context_data(self, **kwargs):
      context = super(IWatchDetailView, self).get_context_data(**kwargs)
      context['IWatch'] = self.get_object()
      items = list(IWatch.objects.all())
      # change 3 to how many random items you want
      random_objects = random.sample(items, 8)
      context['random_objects'] = random_objects
      context['seektime'] = 10
      return context



class TopWatchedView(ListView):
  model = IWatch
  template_name = 'IWatch/top_watched.html'
  # count_hit = True

  def get_context_data(self, **kwargs):
      context = super(TopWatchedView, self).get_context_data(**kwargs)
      context.update({
          'top_watched': IWatch.objects.order_by('-hit_count_generic__hits'),
      })
      return context




class SearchIWatch(ListView):

  def get(self, request, *args, **kwargs):
    query = self.request.GET.get('query').strip()
    if query:
      print("************************", query)
      IWatch_list = IWatch.objects.filter(
        Q(creator__user__username__contains=query) | 
        Q(creator__user__full_name__icontains=query) | 
        Q(title__icontains=query) |
        Q(description__icontains=query)
      )    
      context = {
        'IWatch_list': IWatch_list,
      }
      return render(request, "IWatch/Search.html", context)
    else:
      return redirect(request.META.get('HTTP_REFERER'))
      



# i dn't need views count here
class UploadVideoView(CreateView):
  model = IWatch
  form_class =  IWatchModelForm
  template_name = 'IWatch/upload.html'
  success_url = reverse_lazy('IWatch:IWatch-main')


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
      context = super(IWatchListView, self).get_context_data(**kwargs)
      profile = Profile.objects.get(user=self.request.user)
      following_users = profile.following.all()
      following_profiles = Profile.objects.filter(user__in=following_users)
      following_profiles |= Profile.objects.filter(user=self.request.user)
      following_Videos = IWatch.objects.filter(creator__in=following_profiles)
      context['qs'] = following_Videos
      context['following_profiles'] = following_profiles.exclude(user=self.request.user)

      # Recommendation system for now
      items = list(IWatch.objects.all())
      people = list(Profile.objects.all())
      # change 8 to how many random items you want
      random_objects = random.sample(items, 8)
      random_people = random.sample(people, 8)
      context['random_objects'] = random_objects
      context['random_people'] = random_people

      # context['IWatch_list'] = IWatch.objects.all()[:5]
      # context['post_views'] = ["ajax", "detail", "detail-with-count"]
      return context


  


@login_required
def create_comment(request):
  ''' It will get comment from js, and return json response! '''
  profile = Profile.objects.get(user=request.user)

  if request.method == 'POST':
    body = request.POST["body"]
    post_id = request.POST['post_id']

    iw = IWatchComment(user=profile, IWatch=IWatch.objects.get(id=post_id), body=body)
    iw.save()
  
    # Notification Corner
    body = iw.body[:50] + '...' # to show only 50 characters in the notification
    if iw.user != iw.IWatch.creator:
      notify.send(request.user, recipient=iw.IWatch.creator.user, verb=body, action_object=iw.IWatch, description='on post ') #{IWatch.post.post_number}

    comments = IWatchComment.objects.filter(IWatch=iw.IWatch).values()
    list_of_comments = list(comments)

    no_of_comments = iw.IWatch.get_total_comments() # comment > IWatch > func :) 
    c_user = iw.user.user.username
    c_body = iw.body
    c_date = iw.created
    data = {
      'status': 'save',
      'c_user': c_user,
      'c_body': c_body,
      'c_date': c_date,
      'no_of_comments': no_of_comments,
      'list_of_comments': list_of_comments,
    }
    # print('data***************\n\n', data.values())
    return JsonResponse(data, safe=False)

  return render(request, "IWatch/showIWatch.html")


@login_required
def like(request):
  '''
  This will handle the like, and will save it recordes in the database.
  'enable_like' = is for internal use, to save repitition of code
  post = is the Object of Post class declared in models.py
  '''
  if request.method == 'POST':
    def enable_like():
      like = Like.objects.create(user=user, IWatch=iw, liked=True)
      # upvote.save()
      iw.liked = iw.liked + 1
      iw.save()

    post_id = request.POST['post_id']
    user= request.user
    iw = IWatch.objects.get(id=post_id) # get the post object

    # check if the user has already upvoted the post
    like = Like.objects.filter(user=user, IWatch=iw, liked=True).first()
    if like != None: # if the user has already upvoted the post
      like.delete() # delete the upvote
      iw.liked = iw.liked - 1
      iw.save()

  
    else:
      # check if the user has already downvoted the post
      dislike = Dislike.objects.filter(user=user, IWatch=iw, disliked=True).first()
      if dislike != None:
        dislike.delete()
        iw.disliked = iw.disliked - 1
        iw.save()
        enable_like()
      else:
        enable_like()

      data = {
        'like': iw.liked,
      }
      return JsonResponse(data, safe=False)
    
    # return JsonResponse(data, safe=False)
  return redirect('IWatch:IWatch-main')

@login_required
def dislike(request):
  '''
  This will handle the like, and will save it recordes in the database.
  'enable_like' = is for internal use, to save repitition of code
  post = is the Object of Post class declared in models.py
  '''
  if request.method == 'POST':
    def enable_dislike():
      dislike = Dislike.objects.create(user=user, IWatch=iw, disliked=True)
      # upvote.save()
      iw.disliked = iw.disliked + 1
      iw.save()

    post_id = request.POST['post_id']
    user= request.user
    iw = IWatch.objects.get(id=post_id) # get the post object

    # check if the user has already upvoted the post
    dislike = Dislike.objects.filter(user=user, IWatch=iw, disliked=True).first()
    if dislike != None: # if the user has already upvoted the post
      dislike.delete() # delete the upvote
      iw.liked = iw.liked - 1
      iw.save()

  
    else:
      # check if the user has already downvoted the post
      like = Like.objects.filter(user=user, IWatch=iw, liked=True).first()
      if like != None:
        like.delete()
        iw.liked = iw.liked - 1
        iw.save()
        enable_dislike()

      else:
        enable_dislike()

      data = {
        'dislike': iw.disliked,
      }
      return JsonResponse(data, safe=False)
    
    # return JsonResponse(data, safe=False)
  return redirect('IWatch:IWatch-main')


class PostDeleteView(DeleteView): 
    model = IWatch
    template_name = 'IWatch/confirm_delete.html'
    success_url = reverse_lazy('IWatch:IWatch-main') 

    # only author will be able to delete the post
    def get_object(self, *args, **kwargs):
      pk = self.kwargs.get('pk')
      obj = IWatch.objects.get(pk=pk)
      if not obj.creator.user == self.request.user:
        messages.warning(self.request, "You are not authorized to delete this post")
      return obj
    

class PostUpdateView(UpdateView):
    model = IWatch
    form_class = IWatchModelForm  # from forms.py
    template_name = 'IWatch/update.html'
    success_url = reverse_lazy('IWatch:IWatch-main')

    # only author will be able to update the post
    def form_valid(self, form):
      profile = Profile.objects.get(user=self.request.user)
      if form.instance.creator == profile:
        return super().form_valid(form)
      else:
        form.add_error(None, "You are not authorized to update this post")
        return super().form_invalid(form)
