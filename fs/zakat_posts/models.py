from django.db import models
from profiles.models import Profile
from IWatch.models import IWatch
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from user.models import User
from phonenumber_field.modelfields import PhoneNumberField



class ZakatPosts(models.Model):
  creator       = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='zakat_posts')
  seeker        = models.CharField(max_length=100, blank=True) 
  phone_number  = PhoneNumberField(null=True, unique=True)
  address       = models.CharField(max_length=150, blank=True)
  bank_details  = models.CharField(max_length=200, blank=True)
  donor         = models.ManyToManyField(Profile, blank=True, related_name='donors') 
  video1        = models.FileField(upload_to='zakat_video', blank=True)
  video2        = models.FileField(upload_to='zakat_video', blank=False)
  varified      = models.IntegerField(default=0, blank=True)
  paid          = models.IntegerField(default=0, blank=True)
  needed_money  = models.IntegerField(default=0, blank=False)
  satisfied     = models.BooleanField(default=False, blank=True)
  upvote        = models.IntegerField(default=0)
  downvote      = models.IntegerField(default=0)
  created       = models.DateTimeField(auto_now_add=True)
  post_number   = models.IntegerField(default=0)
  updated       = models.DateTimeField(auto_now=True)
  content       = models.TextField(blank=True, null=True)

  def __str__(self):
    return str(self.pk)

  def get_num_upvotes(self):
    return self.upvotes.all().count()
  
  def get_num_satified(self):
    return self.satisfied.all().count()

  def get_num_donors(self):
    return self.donors.all().count()

  def get_num_downvotes(self):
    return self.downvotes.all().count()

  def get_total_zp(self):
    return ZakatPosts.objects.all().count()
  
  def get_num_comments(self):
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
  
  def get_users(self):
    return self.user.all()


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

  