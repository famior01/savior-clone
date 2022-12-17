from django.db import models
from profiles.models import Profile
from posts.models import Posts
from django.contrib.auth.models import User

# Create your models here.

class ZakatPosts(models.Model):
  creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
  seeker = models.CharField(max_length=100, blank=True) 
  donor = models.ManyToManyField(Profile, blank=True, related_name='donors') 
  number1 = models.IntegerField(default=0, blank=True)
  cnic1 = models.ImageField(upload_to='cnic_image', blank=True)
  spouse_name = models.CharField(max_length=100, blank=True)
  number2 = models.IntegerField(default=0, blank=True)
  cnic2 = models.ImageField(upload_to='cnic_image', blank=True)
  no_of_children = models.IntegerField(default=0)
  video1 = models.FileField(upload_to='zakat_video', blank=True)
  video2 = models.FileField(upload_to='zakat_video', blank=True)
  AI_varified = models.BooleanField(default=False, blank=True)
  paid = models.BooleanField(default=False, blank=True)
  expected_money = models.IntegerField(default=0)
  upvote = models.IntegerField(default=0)
  downvote = models.IntegerField(default=0)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  content = models.TextField(blank=True)

  def __str__(self):
    return str(self.pk)

  def num_comments(self):
    return self.zakat_posts_comments.all().count() # type: ignore
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
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user}-{self.post}"
  class Meta:
    ordering = ['-created']

class DownVote(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(ZakatPosts, on_delete=models.CASCADE, related_name='downvotes')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user}-{self.post}"

  class Meta:
    ordering = ['-created']

  