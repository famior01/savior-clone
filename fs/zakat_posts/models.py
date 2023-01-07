from django.db import models
from profiles.models import Profile
from posts.models import Posts
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from user.models import User


class ZakatPosts(models.Model):
  creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
  seeker = models.CharField(max_length=100, blank=True) 
  donor = models.ManyToManyField(Profile, blank=True, related_name='donors') 
  video1 = models.FileField(upload_to='zakat_video', blank=True)
  video2 = models.FileField(upload_to='zakat_video', blank=False)
  varified = models.IntegerField(default=0, blank=True)
  paid = models.IntegerField(default=0, blank=True)
  needed_money = models.IntegerField(default=0, blank=False)
  satisfied = models.BooleanField(default=False, blank=True)
  upvote = models.IntegerField(default=0)
  downvote = models.IntegerField(default=0)
  created = models.DateTimeField(auto_now_add=True)
  post_number = models.IntegerField(default=0)
  updated = models.DateTimeField(auto_now=True)
  content = models.TextField(blank=True, null=True)

  def __str__(self):
    return str(self.pk)

  def num_comments(self):
    return self.zakat_posts_comments.all().count() 
  class Meta:
    ordering = ('-created',)


class ZakatPostsComment(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='zakat_posts_user_comments')
  post = models.ForeignKey(ZakatPosts,  on_delete=models.CASCADE, related_name='zakat_posts_comments')
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.pk)
  class Meta:
    ordering = ['-created_at']


class UpVote(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(ZakatPosts, on_delete=models.CASCADE, related_name='upvotes')
  upvoted = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user}-{self.post}"
  class Meta:
    ordering = ['-created']

class DownVote(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(ZakatPosts, on_delete=models.CASCADE, related_name='downvotes')
  downvoted = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user}-{self.post}"

  class Meta:
    ordering = ['-created']

  